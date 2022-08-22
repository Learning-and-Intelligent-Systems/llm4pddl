"""Create a table summarizing results saved to a directory."""

import argparse
import glob
import pickle
from pathlib import Path
from typing import Any, Callable, Dict

import numpy as np
import pandas as pd

from llm4pddl.structs import TaskMetrics

_DERIVED_COLS: Dict[str, Callable[[TaskMetrics], Any]] = {
    "success": lambda d: float(d["result"] == "success")
}


def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results_dir", default="results", type=str)
    args = parser.parse_args()
    raw_results = _load_results(args.results_dir)
    _create_summary_table(raw_results)


def _load_results(results_dir: str) -> pd.DataFrame:
    all_data = []
    git_commit_hashes = set()
    for filepath in sorted(glob.glob(f"{results_dir}/*")):
        with open(filepath, "rb") as f:
            outdata = pickle.load(f)
        git_commit_hashes.add(outdata["git_commit_hash"])
        results = outdata["results"].copy()
        env, approach, seed, experiment_id = Path(filepath).stem.split("__")
        for task_id, task_results in results.items():
            datum = {
                "env": env,
                "approach": approach,
                "seed": seed,
                "experiment_id": experiment_id,
                "task_id": task_id,
                **task_results,
            }
            for col, derive_fn in _DERIVED_COLS.items():
                datum[col] = derive_fn(datum)
            all_data.append(datum)
    if not all_data:
        raise ValueError(f"No data found in {results_dir}/")
    # Group & aggregate data.
    pd.set_option("display.max_rows", 999999)
    df = pd.DataFrame(all_data)
    print(f"Git commit hashes seen in {results_dir}/:")
    for commit_hash in git_commit_hashes:
        print(commit_hash)
    # Uncomment the next line to print out ALL the raw data.
    # print(df)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    return df


def _create_summary_table(raw_results: pd.DataFrame) -> None:
    # Remove the non-numeric columns that we don't need anymore.
    df = raw_results.drop(columns=["result"])
    # Group by env, approach, seed, and experiment ID.
    grouped = df.groupby(["env", "approach", "seed", "experiment_id"])
    # Average over eval tasks.
    eval_means = grouped.mean().reset_index()
    # Get statistics over seed.
    grouped = eval_means.groupby(["env", "approach", "experiment_id"])
    means = grouped.mean()
    stds = grouped.std(ddof=0)
    sizes = grouped.size().to_frame()
    # Add standard deviations to the printout.
    for col in means:
        for row in means[col].keys():
            mean = means.loc[row][col]
            std = stds.loc[row][col]
            means.loc[row, col] = f"{mean:.2f} ({std:.2f})"
    means["num_seeds"] = sizes
    pd.set_option("expand_frame_repr", False)
    print("\n\nAGGREGATED DATA OVER EVAL TASKS AND SEEDS:")
    print(means.reset_index())
    means.to_csv("results_summary.csv")
    print("\n\nWrote out table to results_summary.csv")
    # Report the total number of results.
    print(f"\nTOTAL RESULTS: {df.shape[0]}")
    # Create an even higher-level summary, averaging over everything except
    # the approach.
    print("\nSUMMARY OF THE SUMMARY:")
    print(df.groupby(["approach"]).mean())


if __name__ == "__main__":
    _main()
