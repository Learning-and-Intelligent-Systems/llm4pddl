"""An approach that use a large language model to solve tasks."""

import logging
from typing import Dict, List, Optional, Tuple

from llm4pddl import utils
from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.flags import FLAGS
from llm4pddl.llm_interface import OpenAILLM
from llm4pddl.structs import Dataset, LLMResponse, Plan, PyperplanObject, \
    PyperplanType, Task, TaskMetrics


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

    @property
    def is_learning_based(self) -> bool:
        return True

    @property
    def is_planning_based(self) -> bool:
        return False

    def get_name(self) -> str:
        return "llm-open-loop"

    def solve(self, task: Task) -> Tuple[Optional[Plan], TaskMetrics]:
        new_prompt = self._create_prompt(task, [])  # empty partial plan
        prompt = self._prompt_prefix + new_prompt
        logging.debug(f"Querying with prompt suffix:\n{new_prompt}")
        responses = self._llm.sample_completions(
            prompt=prompt,
            temperature=self._temperature,
            seed=FLAGS.seed,
            num_completions=self._num_completions)
        return self._llm_responses_to_plan(responses, task)

    def train(self, dataset: Dataset) -> None:
        prompts = []
        for datum in dataset:
            prompt = self._create_prompt(datum.task, datum.solution)
            prompts.append(prompt)
        self._prompt_prefix = "\n\n".join(prompts) + "\n\n"
        logging.debug(f"Created prompt prefix:\n{self._prompt_prefix}")

    @staticmethod
    def _create_prompt(task: Task, plan: Plan) -> str:
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
        objects_strs: List[str] = []
        for typ, objs in type_to_objs.items():
            if not objs:
                continue
            typ_str = " ".join(objs) + " - " + str(typ)
            objects_strs.append(typ_str)
        objects_str = "\n  ".join(objects_strs)
        # Create the init string.
        init_str = "\n".join(
            utils.pred_to_str(p) for p in problem.initial_state)
        # Create the goal string.
        goal_str = "\n".join(utils.pred_to_str(p) for p in problem.goal)
        # Create the solution string.
        solution_str = "\n  ".join(plan)
        prompt = f"""(:objects
  {objects_str}
)
(:init
  {init_str}
)
(:goal
  {goal_str}
)
solution:
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
            # If there's nothing in between, the response is malformed.
            if not words:
                break
            # The first word should be an operator.
            op, objects = words[0], words[1:]
            if op not in operator_names:
                break
            # The remaining words should be objects.
            if any(o not in object_names for o in objects):
                break
            # The signature of the objects should match that of the operator.
            op_sig = [t for _, (t, ) in domain.actions[op].signature]
            objs_sig = [obj_to_type[o] for o in objects]
            if len(op_sig) != len(objs_sig) or not all(
                    utils.is_subtype(t1, t2)
                    for (t1, t2) in zip(objs_sig, op_sig)):
                break
            # Otherwise, we found a good plan step.
            objects_str = " ".join(objects)
            action = f"({op} {objects_str})"
            plan.append(action)
            # Update the unparsed response.
            unparsed = unparsed[right_parens_idx + 1:]
        return plan