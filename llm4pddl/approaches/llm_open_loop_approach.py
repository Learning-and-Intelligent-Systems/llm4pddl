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
from llm4pddl.structs import Any, Dataset, Datum, Embedding, LLMResponse, \
    Plan, PyperplanObject, PyperplanType, Task, TaskMetrics


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
        # {'embedding': Embedding, 'datum': Datum}, representing a Datum
        # in the training set and that datum's task string's embedding.
        self._list_embeddings_mapping: List[Dict[str, Any]] = []
        self._embedding_model = SentenceTransformer(FLAGS.embedding_model_name)

    @property
    def is_learning_based(self) -> bool:
        return True

    @property
    def is_planning_based(self) -> bool:
        return False

    def get_name(self) -> str:
        return "llm-open-loop"

    def solve(self, task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        new_prompt = self._create_prompt(task)
        if FLAGS.use_dynamic_examples:
            closest_datums = self._get_closest_datums(
                task, self._list_embeddings_mapping, FLAGS.num_train_tasks)
            self._create_prompt_prefix(closest_datums)
        prompt = self._prompt_prefix + new_prompt
        logging.debug(f"Querying with prompt suffix:\n{new_prompt}")
        if FLAGS.llm_autoregressive_prompting:
            metrics: TaskMetrics = {}
            # Since auto-regressive prompting will lead to divergent queries,
            # we need to just prompt separately once per num_completions.
            # Furthermore, to get variance, we need to disable the cache.
            disable_cache = (self._num_completions > 1)
            for _ in range(self._num_completions):
                plan = self._prompt_autoregressive(prompt, task, disable_cache)
                # Return immediately if we succeeded.
                if plan is not None:
                    return plan, metrics
            # We failed, give up.
            return None, metrics
        responses = self._llm.sample_completions(
            prompt=prompt,
            temperature=self._temperature,
            seed=FLAGS.seed,
            stop_token=utils.LLM_QUESTION_TOKEN,  # start of next question
            num_completions=self._num_completions)
        return self._llm_responses_to_plan(responses, task)

    def train(self, dataset: Dataset) -> None:
        self._create_prompt_prefix(dataset)
        # Embedding the training tasks:
        if FLAGS.use_dynamic_examples:
            train_tasks = [datum.task for datum in dataset]
            embeddings = self._embed_tasks(train_tasks)
            self._list_embeddings_mapping = self._make_embeddings_mapping(
                embeddings, dataset)

    def _create_prompt_prefix(self, dataset: Dataset) -> None:
        prompts = []
        for datum in dataset:
            prompt = self._create_prompt(datum.task, datum.solution)
            prompts.append(prompt)
        self._prompt_prefix = "\n\n".join(prompts) + "\n\n"
        logging.debug(f"Created prompt prefix:\n{self._prompt_prefix}")

    @staticmethod
    def _create_prompt(task: Task, plan: Optional[Plan] = None) -> str:
        """Create a prompt entry for a single task and (maybe partial) plan."""
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
        return prompt

    def _llm_responses_to_plan(
            self, responses: List[LLMResponse],
            task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        # Return the first plan that succeeds. Subclasses may override.
        # By default, this class doesn't plan, so there are no metrics.
        metrics: TaskMetrics = {}
        for response in responses:
            logging.debug(f"Processing response:\n{response.response_text}")
            plan = self._llm_response_to_plan(response.response_text, task)
            if utils.validate_plan(task, plan):
                return plan, metrics
        return None, metrics

    @staticmethod
    def _llm_response_to_plan(response_text: str,
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
            # The first word should be an operator.
            op, objects = words[0], words[1:]
            if not disable_name_checks and op not in operator_names:
                continue
            # The remaining words should be objects.
            if not disable_name_checks and any(o not in object_names
                                               for o in objects):
                continue
            # The signature of the objects should match that of the operator.
            op_sig = [t for _, (t, ) in domain.actions[op].signature]
            objs_sig = [obj_to_type[o] for o in objects]
            if not disable_name_checks and len(op_sig) != len(
                    objs_sig) or not all(
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
                               disable_cache: bool = False) -> Optional[Plan]:
        """Prompt the LLM for one action at a time."""
        pyperplan_task = utils.get_pyperplan_task(task)
        ground_ops = {o.name: o for o in pyperplan_task.operators}
        # Loop until the next question token is reached, or an invalid response
        # is returned. Note that this will terminate at most when the maximum
        # token length is reached, in which case an empty (invalid) response
        # will be returned by the LLM.
        last_plan: Plan = []
        cumulative_response = ""
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
            assert len(responses) == 1
            response = responses[0].response_text + ")"
            cumulative_response += response
            # Handle syntax.
            plan = self._llm_response_to_plan(cumulative_response,
                                              task,
                                              disable_name_checks=True)
            assert len(plan) <= len(last_plan) + 1
            # Failed to find a new action.
            if len(plan) == len(last_plan):
                break
            action_str = plan[-1]
            logging.debug(f"Autoregressive parsed output: {action_str}")
            # Check if the action is valid.
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
                new_action_str = max(applicable_actions, key=action_to_sim.get)
                score = action_to_sim[new_action_str]
                logging.debug(f"Replacing inapplicable {action_str} with "
                              f"{new_action_str} (score={score})")
                action_str = new_action_str
            ground_op = ground_ops[action_str]
            prompt += sep + action_str
            current_facts = ground_op.apply(current_facts)
            # Check for success.
            if utils.validate_plan(task, plan, verbose=False):
                return plan
            # Check if the last plan is no different from this one.
            if len(last_plan) == len(plan):
                break
            last_plan = plan
        # Failed.
        return None

    def _embed_task(self, task: Task) -> Embedding:
        """Embeds a task using embedding_model."""
        # note: task_string includes the Q: and A: parts, not just task string
        task_string = self._create_prompt(task)
        embedding = self._embedding_model.encode(task_string)
        return embedding

    def _embed_tasks(self, tasks: List[Task]) -> List[Embedding]:
        """"Embeds a list of tasks.

        Returns a list of embeddings with indices corresponding to its
        task.
        """
        embeddings = [self._embed_task(task) for task in tasks]
        return embeddings

    @functools.lru_cache(maxsize=None)
    def _embed_str_with_cache(self, s: str) -> Embedding:
        return self._embedding_model.encode(s)

    def _make_embeddings_mapping(self, embeddings: List[Embedding],
                                 dataset: Dataset) -> List[Dict[str, Any]]:
        """Makes embeddings mapping for training data."""
        assert len(embeddings) == len(dataset)
        return [{
            'embedding': emb,
            'datum': datum
        } for emb, datum in zip(embeddings, dataset)]

    def _get_closest_datums(self, task: Task,
                            embeddings_mapping: List[Dict[str, Any]],
                            num_closest: int) -> List[Datum]:
        """Returns the num_closest most similar training tasks to the task, in
        order of from least to most similar."""
        assert num_closest <= len(embeddings_mapping)
        task_embedding = self._embed_task(task)
        # now compare this embedding to all the other embeddings
        other_embeddings = [
            mapping['embedding'] for mapping in embeddings_mapping
        ]
        cos_sims = [
            self._get_cosine_sim(task_embedding, other_emb)
            for other_emb in other_embeddings
        ]
        # we will need a get_init_string() and get_goal_string() helper funcs.
        indices = np.argsort(cos_sims)[-num_closest:]
        closest_datums = [embeddings_mapping[ind]['datum'] for ind in indices]
        return closest_datums

    def _get_cosine_sim(self, embedding1: Embedding,
                        embedding2: Embedding) -> float:
        """Returns the cosine similarity between the two embeddings."""
        return cos_sim(embedding1, embedding2).item()
