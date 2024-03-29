"""An approach that use a large language model to solve tasks."""

import functools
import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from llm4pddl import utils
from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.flags import FLAGS
from llm4pddl.llm_interface import OpenAILLM
from llm4pddl.structs import Any, Dataset, Datum, Embedding, Plan, \
    PromptSubstitution, PyperplanObject, PyperplanType, Task, TaskMetrics


class LLMOpenLoopApproach(BaseApproach):
    """An approach that simply queries the LLM to solve tasks."""

    def __init__(self, num_completions: int, temperature: float) -> None:
        super().__init__()
        # Set up the LLM.
        self._num_completions = num_completions
        self._temperature = temperature
        self._llm = OpenAILLM(FLAGS.llm_model_name)
        # Set after learning.
        self._prompt_prefix = ""
        # _list_embeddings_mapping is a list of dictionaries of the form
        # {'init_emb': Embedding, 'datum': Datum, 'goal_emb: Embedding},
        # representing a Datum in the training set and that datum's
        # init string embedding and goal string embedding.
        self._list_embeddings_mapping: List[Dict[str, Any]] = []
        self._embedding_model = SentenceTransformer(FLAGS.embedding_model_name)
        # Reset on every call to solve().
        self._eval_task_str_subs = PromptSubstitution(objects={},
                                                      operators={},
                                                      predicates={},
                                                      types={})
        # Created on the first call to create_prompt().
        self._op_subs: Optional[Dict[str, str]] = None
        self._pred_subs: Optional[Dict[str, str]] = None
        self._type_subs: Optional[Dict[str, str]] = None

    @property
    def is_learning_based(self) -> bool:
        return True

    @property
    def is_planning_based(self) -> bool:
        return False

    def get_name(self) -> str:
        return "llm-open-loop"

    def solve(self, task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        new_prompt, subs = self._create_prompt(task)
        # Store the substitutions for this eval task so that we can invert
        # the LLM response in _llm_response_to_plan().
        self._eval_task_str_subs = subs
        if FLAGS.use_dynamic_examples:
            closest_datums = self._get_closest_datums(
                task, self._list_embeddings_mapping, FLAGS.num_train_tasks)
            self._create_prompt_prefix(closest_datums)
        prompt = self._prompt_prefix + new_prompt
        logging.debug(f"Querying with prompt suffix:\n{new_prompt}")
        partial_plans = []
        if FLAGS.llm_autoregressive_prompting:
            assert not FLAGS.llm_use_random_plans
            # Since auto-regressive prompting will lead to divergent queries,
            # we need to just prompt separately once per num_completions.
            # Furthermore, to get variance, we need to disable the cache.
            disable_cache = self._num_completions > 1
            for _ in range(self._num_completions):
                plan = self._prompt_autoregressive(prompt, task, disable_cache)
                partial_plans.append(plan)
        elif FLAGS.llm_use_random_plans:
            # An ablation where we sample random plans instead of querying
            # the LLM. For apples-to-apples comparing, we get the length of
            # the plan output by the main llm-standard method and then get
            # a random plan of the same length.
            autoregressive_plan = self._prompt_autoregressive(
                prompt, task, disable_cache=False)
            max_steps = len(autoregressive_plan)
            for _ in range(self._num_completions):
                plan = utils.get_random_partial_plan(task, self._rng,
                                                     max_steps)
                partial_plans.append(plan)
        else:
            responses = self._llm.sample_completions(
                prompt=prompt,
                temperature=self._temperature,
                seed=FLAGS.seed,
                stop_token=utils.LLM_QUESTION_TOKEN,  # start of next question
                num_completions=self._num_completions)
            # Turn each response into a sequence of actions.
            for response in responses:
                response_text = response.response_text
                logging.debug(f"Processing response:\n{response_text}")
                partial_plan = self._llm_response_to_plan(response_text, task)
                partial_plans.append(partial_plan)
        return self._solve_from_partial_plans(partial_plans, task)

    def train(self, dataset: Dataset) -> None:
        self._create_prompt_prefix(dataset)
        # Embedding the training tasks:
        if FLAGS.use_dynamic_examples:
            train_tasks = [datum.task for datum in dataset]
            embeddings = self._embed_tasks(train_tasks)
            self._list_embeddings_mapping = self._make_embeddings_mapping(
                embeddings, dataset)

    def _create_prompt_prefix(self, dataset: Dataset) -> None:
        """Creates prompt prefix for the approach.

        As of now, the 'best' example in  dynamic is used first in the
        prompt, not last.
        """
        prompts = []
        prompt_dataset = dataset[:FLAGS.num_prompt_tasks]
        for datum in prompt_dataset:
            # We do not need to store the substitutions because we will never
            # invert the prompt prefix.
            prompt, _ = self._create_prompt(datum.task, datum.solution)
            prompts.append(prompt)
        self._prompt_prefix = "\n\n".join(prompts) + "\n\n"
        logging.debug(f"Created prompt prefix:\n{self._prompt_prefix}")

    def _create_prompt(
            self,
            task: Task,
            plan: Optional[Plan] = None) -> Tuple[str, PromptSubstitution]:
        """Create a prompt entry for a single task and (maybe partial) plan.

        The second return value keeps track of any substitutions that
        were made in creating the prompt, based on FLAGS. These
        substitutions are then used to invert the LLM response.
        """
        # Extract only the objects, init, and goal from the problem file,
        # stripping out any comments or other extraneous text.
        domain, problem = utils.parse_task(task)
        # Create the objects string.
        type_to_objs: Dict[PyperplanType, List[PyperplanObject]] = {
            t: []
            for t in domain.types.values()
        }
        for obj in sorted(problem.objects):
            obj_type = problem.objects[obj]
            type_to_objs[obj_type].append(obj)
        # Include constants too.
        for obj in sorted(domain.constants):
            obj_type = domain.constants[obj]
            type_to_objs[obj_type].append(obj)
        # Randomize object names.
        if FLAGS.llm_randomize_object_names:
            obj_names = {o for objs in type_to_objs.values() for o in objs}
            obj_subs = utils.create_random_word_substitution(
                obj_names, self._rng)
        else:
            obj_subs = {}
        # Randomize operator names.
        if FLAGS.llm_randomize_operator_names:
            # Note: unlike objects, we want to do this only once per domain!
            op_names = set(domain.actions)
            if self._op_subs is None:
                self._op_subs = utils.create_random_word_substitution(
                    op_names, self._rng)
            assert op_names == set(self._op_subs)
        else:
            self._op_subs = {}
        # Randomize predicate names.
        if FLAGS.llm_randomize_predicate_names:
            # Note: unlike objects, we want to do this only once per domain!
            pred_names = set(domain.predicates)
            if self._pred_subs is None:
                self._pred_subs = utils.create_random_word_substitution(
                    pred_names, self._rng)
            assert pred_names == set(self._pred_subs)
        else:
            self._pred_subs = {}
        # Randomize type names.
        if FLAGS.llm_randomize_type_names:
            # Note: unlike objects, we want to do this only once per domain!
            type_names = set(domain.types)
            if self._type_subs is None:
                self._type_subs = utils.create_random_word_substitution(
                    type_names, self._rng)
            assert type_names == set(self._type_subs)
        else:
            self._type_subs = {}
        # Construct the object list for the prompt.
        objects_strs: List[str] = []
        for typ, objs in type_to_objs.items():
            if not objs:
                continue
            typ_str = " ".join(objs) + " - " + str(typ)
            objects_strs.append(typ_str)
        # Create the objects string.
        objects_str = "\n  ".join(objects_strs)
        # Create the solution string.
        if plan is None:
            solution_str = utils.LLM_ANSWER_TOKEN
        else:
            plan_str = "\n  ".join(plan)
            solution_str = utils.LLM_ANSWER_TOKEN + "\n" + plan_str
        if FLAGS.llm_prompt_method == "standard":
            # Create the init string.
            init_str = utils.get_init_str(task)
            # Create the goal string.
            goal_str = utils.get_goal_str(task)
        else:
            assert FLAGS.llm_prompt_method == "group-by-predicate"
            # Create the init string.
            init_str_groups = utils.group_by_predicate(problem.initial_state)
            init_str = "\n".join(sorted(init_str_groups))
            # Create the goal string.
            goal_str_groups = utils.group_by_predicate(problem.goal)
            goal_str = "\n".join(sorted(goal_str_groups))
        # Create the prompt.
        prompt = f"""{utils.LLM_QUESTION_TOKEN}
    (:objects
    {objects_str}
    )
    (:init
    {init_str}
    )
    (:goal
    {goal_str}
    )
    {solution_str}"""
        # Minify the prompt to reduce tokens.
        prompt = utils.minify_pddl_problem(prompt)
        # Finalize the substitutions.
        subs = PromptSubstitution(objects=obj_subs,
                                  operators=self._op_subs,
                                  predicates=self._pred_subs,
                                  types=self._type_subs)
        prompt = utils.substitute_in_prompt(prompt, subs)
        return prompt, subs

    def _solve_from_partial_plans(
            self, partial_plans: List[Plan],
            task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        # Return the first plan that succeeds. Subclasses may override.
        # By default, this class doesn't plan, so there are no metrics.
        metrics: TaskMetrics = {}
        for plan in partial_plans:
            if utils.validate_plan(task, plan):
                return plan, metrics
        return None, metrics

    def _llm_response_to_plan(self,
                              response_text: str,
                              task: Task,
                              disable_name_checks: bool = False) -> Plan:
        # We assume the LLM's output is such that each line contains
        # (operator-name object1-name object2-name ...) with optional
        # whitespace allowed everywhere. Furthermore, the signature of the
        # objects should match the operator. As soon as these assumptions are
        # violated, we stop parsing and return whatever plan has been parsed
        # up to that point.
        domain, problem = utils.parse_task(task)
        operator_names = set(domain.actions)
        object_names = set(problem.objects) | set(domain.constants)
        obj_to_type = {**problem.objects, **domain.constants}
        plan: Plan = []
        unparsed = response_text
        # Make sure we don't go past the next question.
        if utils.LLM_QUESTION_TOKEN in unparsed:
            unparsed, _ = unparsed.split(utils.LLM_QUESTION_TOKEN, 1)
        while "(" in unparsed:
            left_parens_idx = unparsed.index("(")
            # If there is no matching ), the response is malformed.
            if ")" not in unparsed:
                break
            right_parens_idx = unparsed.index(")")
            # If a ) appears before a (, the response is malformed.
            if right_parens_idx < left_parens_idx:
                break
            # Get the words in between the parentheses.
            words = unparsed[left_parens_idx + 1:right_parens_idx].split()
            # Update the unparsed response.
            # Now that we have updated the unparsed response, from here on, if
            # there is an issue encountered with the present action, we will
            # continue, rather than break, and hope that there are still good
            # actions to be had later on in the plan.
            unparsed = unparsed[right_parens_idx + 1:]
            # If there's nothing in between, the response is malformed.
            if not words:
                continue
            op, objects = words[0], words[1:]
            # Invert the operator name using the substitutions.
            rev_op_subs = {
                v: k
                for k, v in self._eval_task_str_subs.operators.items()
            }
            if op in rev_op_subs:
                op = rev_op_subs[op]
            # Invert the object names using the substitutions.
            inverted_objects = []
            rev_obj_subs = {
                v: k
                for k, v in self._eval_task_str_subs.objects.items()
            }
            for obj in objects:
                if obj in rev_obj_subs:
                    inverted_objects.append(rev_obj_subs[obj])
                else:
                    inverted_objects.append(obj)
            objects = inverted_objects
            # Check the names of the objects and operators.
            if not disable_name_checks:
                # The first word should be an operator.
                if op not in operator_names:
                    continue
                # The remaining words should be objects.
                if any(o not in object_names for o in objects):
                    continue
                # The signature of the objects should match the operator.
                op_sig = [t for _, (t, ) in domain.actions[op].signature]
                objs_sig = [obj_to_type[o] for o in objects]
                if len(op_sig) != len(objs_sig) or not all(
                        utils.is_subtype(t1, t2)
                        for (t1, t2) in zip(objs_sig, op_sig)):
                    continue
            # Otherwise, we found a good plan step.
            objects_str = " ".join(objects)
            action = f"({op} {objects_str})"
            plan.append(action)
        return plan

    def _prompt_autoregressive(self,
                               prompt: str,
                               task: Task,
                               disable_cache: bool = False) -> Plan:
        """Prompt the LLM for one action at a time."""
        pyperplan_task = utils.get_pyperplan_task(task)
        ground_ops = {o.name: o for o in pyperplan_task.operators}
        # Loop until the next question token is reached, or an invalid response
        # is returned. Note that this will terminate at most when the maximum
        # token length is reached, in which case an empty (invalid) response
        # will be returned by the LLM.
        plan: Plan = []
        current_facts = pyperplan_task.initial_state
        sep = "" if FLAGS.llm_prompt_flatten_pddl else "\n"
        for _ in range(FLAGS.llm_autoregress_max_loops):
            # Note: since the prompts are potentially different, we have to
            # query the LLM once per num_completion.
            responses = self._llm.sample_completions(
                prompt=prompt,
                temperature=self._temperature,
                seed=FLAGS.seed,
                stop_token=")",  # end of the action
                num_completions=1,  # num_completions handled in outer loop
                disable_cache=disable_cache)
            if not responses:
                break
            assert len(responses) == 1
            response = responses[0].response_text + ")"
            # Handle syntax.
            response_plan = self._llm_response_to_plan(
                response, task, disable_name_checks=True)
            # No valid response from LLM, give up.
            if not response_plan:
                break
            # Should be guaranteed 1 because the LLM will stop at ")".
            assert len(response_plan) == 1
            action_str = response_plan[0]
            logging.debug(f"Autoregressive parsed output: {action_str}")
            # If the action is invalid, replace it with the nearest valid one.
            if (action_str not in ground_ops) or (
                    not ground_ops[action_str].applicable(current_facts)):
                # Find the nearest applicable action.
                applicable_actions = {
                    op
                    for op in ground_ops
                    if ground_ops[op].applicable(current_facts)
                }
                # If there's a dead end, give up. Rare.
                if not applicable_actions:  # pragma: no cover
                    break
                # Find the closest next action.
                out_emb = self._embed_str_with_cache(action_str)
                action_to_emb = {
                    a: self._embed_str_with_cache(a)
                    for a in applicable_actions
                }
                action_to_sim = {
                    a: self._get_cosine_sim(out_emb, act_emb)
                    for a, act_emb in action_to_emb.items()
                }
                # Replace the output with the most similar applicable act.
                new_action_str = max(applicable_actions,
                                     key=action_to_sim.get)  # type: ignore
                score = action_to_sim[new_action_str]
                logging.debug(f"Replacing inapplicable {action_str} with "
                              f"{new_action_str} (score={score})")
                action_str = new_action_str
            # Update the prompt with action_str. This is the autoregress.
            prompt_action_str = action_str
            # If we're randomizing object names, need to map them back.
            obj_subs = self._eval_task_str_subs.objects
            for k, v in obj_subs.items():  # pragma: no cover
                prompt_action_str = prompt_action_str.replace(k, v)
            # If we're randomizing operator names, need to map back.
            op_subs = self._eval_task_str_subs.operators
            for k, v in op_subs.items():  # pragma: no cover
                prompt_action_str = prompt_action_str.replace(k, v)
            prompt += sep + prompt_action_str
            # Update the plan.
            plan.append(action_str)
            # Update the current facts for the next applicability checks.
            ground_op = ground_ops[action_str]
            current_facts = ground_op.apply(current_facts)
            # Check for success.
            if utils.validate_plan(task, plan, verbose=False):
                return plan
        # Failed.
        failed_plan_str = "\n".join(plan)
        logging.debug("Autoregressive prompting failed. Final failed plan: "
                      f"{failed_plan_str}")
        return plan

    def _embed_task(self, task: Task) -> Dict[str, Embedding]:
        """Embeds a task using embedding_model."""
        # note: task_string includes the Q: and A: parts, not just task string
        init_str = utils.get_init_str(task)
        goal_str = utils.get_goal_str(task)
        init_embedding = self._embedding_model.encode(init_str)
        goal_embedding = self._embedding_model.encode(goal_str)
        return {'init': init_embedding, 'goal': goal_embedding}

    def _embed_tasks(self, tasks: List[Task]) -> List[Dict[str, Embedding]]:
        """"Embeds a list of tasks.

        Returns a list of embeddings with indices corresponding to its
        task.
        """
        embeddings = [self._embed_task(task) for task in tasks]
        return embeddings

    @functools.lru_cache(maxsize=None)
    def _embed_str_with_cache(self, s: str) -> Embedding:
        return self._embedding_model.encode(s)

    def _make_embeddings_mapping(self, embeddings: List[Dict[str, Embedding]],
                                 dataset: Dataset) -> List[Dict[str, Any]]:
        """Makes embeddings mapping for training data."""
        assert len(embeddings) == len(dataset)
        return [{
            'init_emb': emb['init'],
            'goal_emb': emb['goal'],
            'datum': datum
        } for emb, datum in zip(embeddings, dataset)]

    def _get_closest_datums(self, task: Task,
                            embeddings_mapping: List[Dict[str, Any]],
                            num_closest: int) -> List[Datum]:
        """Returns the num_closest most similar training tasks to the task, in
        order of from most to least similar."""
        assert num_closest <= len(embeddings_mapping)
        embeddings = self._embed_task(task)

        total_cos_sims = np.array(
            [0.0 for _ in range(len(embeddings_mapping))])

        # finding cos sims for init str:
        task_init_embedding = embeddings['init']
        other_init_embeddings = [
            mapping['init_emb'] for mapping in embeddings_mapping
        ]
        init_cos_sims = np.array([
            self._get_cosine_sim(task_init_embedding, other_emb)
            for other_emb in other_init_embeddings
        ])
        total_cos_sims += init_cos_sims

        # finding cos sims for goal str:
        task_goal_embedding = embeddings['goal']
        other_goal_embeddings = [
            mapping['goal_emb'] for mapping in embeddings_mapping
        ]
        goal_cos_sims = np.array([
            self._get_cosine_sim(task_goal_embedding, other_emb)
            for other_emb in other_goal_embeddings
        ])
        total_cos_sims += goal_cos_sims

        indices = np.argsort(total_cos_sims)[-num_closest:]
        closest_datums = [embeddings_mapping[ind]['datum'] for ind in indices]
        # closest_datums is currently ordered least to most similar
        # we flip it here:
        closest_datums.reverse()
        return closest_datums

    def _get_cosine_sim(self, embedding1: Embedding,
                        embedding2: Embedding) -> float:
        """Returns the cosine similarity between the two embeddings."""
        return cos_sim(embedding1, embedding2).item()
