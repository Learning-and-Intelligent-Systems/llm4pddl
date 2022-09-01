"""An approach that use a large language model to solve tasks."""

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
        self._list_embeddings_mapping: List[Dict] = []

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
            closest_datums = self.get_closest_datums(
                task, self._list_embeddings_mapping, FLAGS.num_train_tasks)
            self._create_prompt_prefix(closest_datums)
        prompt = self._prompt_prefix + new_prompt
        logging.debug(f"Querying with prompt suffix:\n{new_prompt}")
        responses = self._llm.sample_completions(
            prompt=prompt,
            temperature=self._temperature,
            seed=FLAGS.seed,
            num_completions=self._num_completions)
        return self._llm_responses_to_plan(responses, task)

    def train(self, dataset: Dataset) -> None:
        self._create_prompt_prefix(dataset)
        # Embedding the training tasks:
        if FLAGS.use_dynamic_examples:
            train_tasks = [datum.task for datum in dataset]
            embeddings = self.embed_tasks(train_tasks)
            self._list_embeddings_mapping = self.make_embeddings_mapping(
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
            init_strs = [utils.pred_to_str(p) for p in problem.initial_state]
            init_str = "\n".join(init_strs)
            # Create the goal string.
            goal_strs = [utils.pred_to_str(p) for p in problem.goal]
            goal_str = "\n".join(goal_strs)
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
            plan = self._llm_response_to_plan(response, task)
            if utils.validate_plan(task, plan):
                return plan, metrics
        return None, metrics

    @staticmethod
    def _llm_response_to_plan(response: LLMResponse, task: Task) -> Plan:
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
        unparsed = response.response_text
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
            if op not in operator_names:
                continue
            # The remaining words should be objects.
            if any(o not in object_names for o in objects):
                continue
            # The signature of the objects should match that of the operator.
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

    def embed_task(self, task: Task,
                   embedding_model: SentenceTransformer) -> Embedding:
        """Embeds a task using embedding_model.

        Returns a numpy array.
        """
        # note: task_string includes the Q: and A: parts, not just task string
        task_string = self._create_prompt(task)
        # this line is a work around for now:
        task_string = task_string.split('\n')[1:-2][0]
        embedding = embedding_model.encode(task_string)
        return embedding

    def embed_tasks(self, tasks: List[Task]) -> List[Embedding]:
        """"Embeds a list of tasks.

        Returns a list of embeddings with indices corresponding to its
        task.
        """
        embedding_model = SentenceTransformer(FLAGS.embedding_model_name)
        embeddings = [self.embed_task(task, embedding_model) for task in tasks]
        return embeddings

    def make_embeddings_mapping(self, embeddings: List[Embedding],
                                dataset: Dataset) -> List[Dict[str, Any]]:
        """Makes embeddings mapping for training data."""
        assert len(embeddings) == len(dataset)
        return [{
            'embedding': emb,
            'datum': datum
        } for emb, datum in zip(embeddings, dataset)]

    def get_closest_datums(self, task: Task,
                           embeddings_mapping: List[Dict[str, Any]],
                           num_closest: int) -> List[Datum]:
        """Returns the num_train most similar training tasks to the task, in
        reverse order of similarity."""
        assert num_closest <= len(embeddings_mapping)
        embedding_model = SentenceTransformer(FLAGS.embedding_model_name)
        task_embedding = self.embed_task(task, embedding_model)
        # now compare this embedding to all the other embeddings
        other_embeddings = [
            mapping['embedding'] for mapping in embeddings_mapping
        ]
        cos_sims = [
            self.get_cosine_sim(task_embedding, other_emb)
            for other_emb in other_embeddings
        ]
        # we will need a get_init_string() and get_goal_string() helper funcs.
        indicies = np.argsort(cos_sims)[-num_closest:]
        print(f'indicies:{indicies}')
        closest_datums = [embeddings_mapping[ind]['datum'] for ind in indicies]
        return closest_datums

    def get_cosine_sim(self, embedding1: Embedding,
                       embedding2: Embedding) -> float:
        """Returns the cosine similarity between the two embeddings."""
        return cos_sim(embedding1, embedding2).item()
