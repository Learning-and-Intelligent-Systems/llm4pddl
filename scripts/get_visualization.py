"""Creates a collection of graphs summarizing results saved to a directory."""
import argparse
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import pandas as pd

CUSTOM_APPROACHES = ["llm-standard-plan", "llm-multi", "llm-multi-plan"]
BASELINE_APPROACHES = ["fd", "pyperplan"]


def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str)
    parser.add_argument("--output_path", type=str)
    args = parser.parse_args()
    custom_approaches, baseline_approaches = _construct_dictionaries(
        args.input_path)
    _get_visualization(custom_approaches, baseline_approaches,
                       args.output_path)


def _construct_dictionaries(input_path: str) -> Tuple[Dict, Dict]:
    custom_approaches: Dict = {}
    for name in CUSTOM_APPROACHES:
        custom_approaches[name] = {}
    baseline_approaches: Dict = {}
    for name in BASELINE_APPROACHES:
        baseline_approaches[name] = {}

    df = pd.read_csv(input_path)
    column_labels = list(df.columns)
    env_column_index = column_labels.index('env')
    approach_column_index = column_labels.index('approach')
    accuracy_column_index = column_labels.index('success')
    experiment_name_index = column_labels.index('experiment_id')

    for _, row_raw in df.iterrows():
        row = row_raw.tolist()
        approach_name = row[approach_column_index]
        environment_name = row[env_column_index]
        accuracy = row[accuracy_column_index]
        accuracy = float(accuracy[0:accuracy.index(' ')])
        experiment_name = row[experiment_name_index]
        for approach in baseline_approaches:
            if approach_name == "pure-planning" and approach in experiment_name:
                baseline_approaches[approach][environment_name] = accuracy
        for approach in custom_approaches:
            if approach_name == approach:
                custom_approaches[approach][environment_name] = accuracy
    return custom_approaches, baseline_approaches


def _get_visualization(custom_approaches: Dict[str, Dict[str, str]],
                       baseline_approaches: Dict[str, Dict[str, str]],
                       output_path: str) -> None:
    fig, axs = plt.subplots(nrows=5, ncols=6, figsize=(30, 25))
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)
    for ax, env in zip(axs.flat,
                       custom_approaches[CUSTOM_APPROACHES[0]].keys()):
        llm_approaches = CUSTOM_APPROACHES + BASELINE_APPROACHES
        llm_accuracies = []
        for approach in custom_approaches:
            llm_accuracies.append(custom_approaches[approach][env])
        for approach in baseline_approaches:
            llm_accuracies.append(baseline_approaches[approach][env])
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
