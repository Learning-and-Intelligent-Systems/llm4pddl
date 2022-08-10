"""Approaches that use a large language model to solve tasks.."""

from typing import Optional, List, Tuple

from llm4pddl import utils
from llm4pddl.approaches.base_approach import BaseApproach
from llm4pddl.flags import FLAGS
from llm4pddl.llm_interface import OpenAILLM
from llm4pddl.structs import Dataset, Plan, Task, TaskMetrics


class LLMOpenLoopApproach(BaseApproach):
    """An approach that simply queries the LLM to solve tasks."""

    def __init__(self) -> None:
        super().__init__()
        # Set up the LLM.
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
        import ipdb; ipdb.set_trace()

    def train(self, dataset: Dataset) -> None:
        prompts = []
        for datum in dataset:
            prompt = self._create_prompt(datum.task, datum.solution)
            prompts.append(prompt)
        self._prompt_prefix = "\n\n".join(prompts) + "\n\n"

    @staticmethod
    def _create_prompt(task: Task, plan: Plan) -> str:
        """Create a prompt entry for a single task and (maybe partial) plan."""
        with open(task.problem_file, "r", encoding="utf-8") as f:
            problem_str = f.read()
        solution_str = "\n  ".join(plan)
        # Make everything lowercase, just in case that's more natural.
        problem_str = problem_str.lower()
        solution_str = solution_str.lower()
        # Extract only the objects, init, and goal from the problem file,
        # stripping out any comments or other extraneous text.
        domain, problem = utils.parse_task(task)
        # Create the objects string.
        type_to_objs = {t: [] for t in domain.types.values()}
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
        init_str = " ".join(utils.pred_to_str(p) for p in problem.initial_state)
        # Create the goal string.
        goal_str = " ".join(utils.pred_to_str(p) for p in problem.goal)
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
        return prompt
