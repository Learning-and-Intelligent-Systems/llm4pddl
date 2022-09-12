"""Creates a collection of graphs to compare the accuracy of approaches in
different environments."""
import argparse
from typing import Dict

import matplotlib.pyplot as plt
from analyze_results import _create_derived_cols, _load_results

APPROACHES = [
    "llm-standard-plan", "llm-multi", "llm-multi-plan", "fd-only",
    "pyperplan-only"
]


def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str)
    parser.add_argument("--output_path", type=str)
    args = parser.parse_args()
    approaches = _construct_dictionaries(args.input_dir)
    _get_visualization(approaches, args.output_path)


def _construct_dictionaries(input_dir: str) -> Dict[str, Dict[str, str]]:
    approaches: Dict = {}
    for name in APPROACHES:
        approaches[name] = {}

    derived_cols = _create_derived_cols(input_dir)
    df = _load_results(input_dir, derived_cols)
    column_labels = list(df.columns)
    env_column_index = column_labels.index('env')
    approach_column_index = column_labels.index('approach_id')
    accuracy_column_index = column_labels.index('success')

    for _, row_raw in df.iterrows():
        row = row_raw.tolist()
        approach_name = row[approach_column_index]
        environment_name = row[env_column_index]
        accuracy = row[accuracy_column_index]
        for approach in APPROACHES:
            if approach_name == approach:
                approaches[approach][environment_name] = accuracy
    return approaches


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
