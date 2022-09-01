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
    sns.lineplot(data=df, x="num_balls", y="solve_time", hue="approach_id")
    plt.savefig("test.png")


def _get_visualization(approaches: Dict[str, Dict[str, str]],
                       output_path: str) -> None:
    fig, axs = plt.subplots(nrows=5, ncols=6, figsize=(30, 25))
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)
    for ax, env in zip(axs.flat, approaches[APPROACHES[0]].keys()):
        llm_approaches = APPROACHES
        llm_accuracies = []
        for approach_dict in approaches.values():
            llm_accuracies.append(approach_dict[env])
        ax.bar(llm_approaches, llm_accuracies, color="blue")
        ax.set_title(env)
        ax.set_ylabel("accuracy")
        ax.set_xticklabels(llm_approaches, rotation=45)
    fig.savefig(output_path,
                facecolor='w',
                bbox_inches="tight",
                pad_inches=0,
                transparent=True)


if __name__ == "__main__":
    _main()
