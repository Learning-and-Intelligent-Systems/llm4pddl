"""Creates a plot for scaling the number of balls in the gripper domain."""

import argparse
import glob
import pickle
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import seaborn as sns
from analyze_results import _DERIVED_COLS, _load_results

from llm4pddl.structs import TaskMetrics


def _get_num_balls(metrics: TaskMetrics) -> str:
    task_id = metrics["task_id"]
    prefix = "gripper-strips__task"
    assert task_id.startswith(prefix)
    task_num = int(task_id[len(prefix):])
    assert 2 <= task_num <= 21
    return (task_num - 1) * 4


def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, default="results")
    parser.add_argument("--output_path", type=str, default="plots")
    args = parser.parse_args()
    derived_cols = _DERIVED_COLS.copy()
    # Note: this assumes that the task generation has not changed.
    derived_cols["num_balls"] = _get_num_balls
    df = _load_results(args.input_dir, derived_cols)
    print(df)
    # Assuming all success.
    assert (df.success == 1.0).all()
    # Create plot.
    plt.figure()
    sns.lineplot(data=df,
                 x="num_balls",
                 y="solve_time",
                 hue="approach_id",
                 style="approach_id",
                 markers=True)
    plt.savefig("test.png")


if __name__ == "__main__":
    _main()
