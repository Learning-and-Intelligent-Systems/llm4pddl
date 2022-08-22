"""Create a table summarizing results saved to a directory."""

import argparse
import glob
import pickle
from pathlib import Path
from typing import Any, Callable, Dict, Set, Tuple

import numpy as np
import pandas as pd

from llm4pddl.structs import TaskMetrics

_DERIVED_COLS: Dict[str, Callable[[TaskMetrics], Any]] = {
    "success": lambda d: float(d["result"] == "success")
}


def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results_dir", default="results", type=str)
    parser.add_argument("--a_dir", type=str)
    parser.add_argument("--b_dir", type=str)
    args = parser.parse_args()
    if args.a_dir:
        assert args.b_dir
        a_summary = _create_summary_table(_load_results(args.a_dir),
                                          verbose=False,
                                          save_summary=False)
        b_summary = _create_summary_table(_load_results(args.b_dir),
                                          verbose=False,
                                          save_summary=False)
        _summarize_diff(a_summary, b_summary)
    else:
        _create_summary_table(_load_results(args.results_dir))


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


def _create_summary_table(raw_results: pd.DataFrame,
                          verbose: bool = True,
                          save_summary: bool = True) -> pd.DataFrame:
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
    summary = means.copy()
    # Add standard deviations to the printout.
    for col in means:
        for row in means[col].keys():
            mean = means.loc[row][col]
            std = stds.loc[row][col]
            summary.loc[row, col] = f"{mean:.2f} ({std:.2f})"
    summary["num_seeds"] = sizes
    pd.set_option("expand_frame_repr", False)
    if verbose:
        print("\n\nAGGREGATED DATA OVER EVAL TASKS AND SEEDS:")
        print(summary.reset_index())
        # Report the total number of results.
        print(f"\nTOTAL RESULTS: {df.shape[0]}")
        # Create an even higher-level summary, averaging over everything except
        # the approach.
        print("\nSUMMARY OF THE SUMMARY:")
        print(df.groupby(["approach"]).mean())
    if save_summary:
        means.to_csv("results_summary.csv")
        print("\n\nWrote out table to results_summary.csv")
    return means.reset_index()


def _summarize_diff(a_df: pd.DataFrame, b_df: pd.DataFrame) -> None:
    # Collect the unique (env, approach, experiment ID) in each df.
    a_ids = {(r.env, r.approach, r.experiment_id) for _, r in a_df.iterrows()}
    b_ids = {(r.env, r.approach, r.experiment_id) for _, r in b_df.iterrows()}

    # Helper to select rows from IDs.
    def _id_to_rows(df: pd.DataFrame, row_id: Tuple[str, str,
                                                    str]) -> pd.DataFrame:
        env, approach, experiment_id = row_id
        return df[((df.env == env) & (df.approach == approach) & \
                   (df.experiment_id == experiment_id))]

    # Helper to get the score from an ID later on.
    def _id_to_score(df: pd.DataFrame,
                     row_id: Tuple[str, str, str]) -> Tuple[float, ...]:
        rows = _id_to_rows(df, row_id)
        assert rows.shape[0] == 1
        success = rows.success.item()
        expanded = rows.nodes_expanded.item()
        return (success, -1 * expanded)  # lower expanded is better

    # Print five cases: same in both; in A but not in B; in B but not in A;
    # better in A than in B; better in B than in A. Here "better" is defined
    # by looking first at success rate and second at number of nodes expanded.
    a_only_ids = a_ids - b_ids
    b_only_ids = b_ids - a_ids
    better_a_ids = set()
    better_b_ids = set()
    same_in_both_ids = set()

    for row_id in a_ids & b_ids:
        a_score = _id_to_score(a_df, row_id)
        b_score = _id_to_score(b_df, row_id)
        if a_score > b_score:
            better_a_ids.add(row_id)
        elif b_score > a_score:
            better_b_ids.add(row_id)
        else:
            same_in_both_ids.add(row_id)

    # Create dataframes for each of the cases.
    def _ids_to_df(row_ids: Set[Tuple[str, str, str]]) -> pd.DataFrame:
        all_entries = []
        for row_id in sorted(row_ids):
            # Collect from a_df.
            if row_id in a_ids:
                rows = _id_to_rows(a_df, row_id)
                assert rows.shape[0] == 1
                entry = rows.to_dict(orient='records')[0]
                entry["VERSION"] = "A"
                all_entries.append(entry)
            # Collect from b_df.
            if row_id in b_ids:
                rows = _id_to_rows(b_df, row_id)
                assert rows.shape[0] == 1
                entry = rows.to_dict(orient='records')[0]
                entry["VERSION"] = "B"
                all_entries.append(entry)
        # Create combined df.
        return pd.DataFrame(all_entries)

    # Print cases.
    print("\n#################### SAME IN BOTH: ###################")
    print(_ids_to_df(same_in_both_ids))

    print("\n##################### ONLY IN A: #####################")
    print(_ids_to_df(a_only_ids))

    print("\n##################### ONLY IN B: #####################")
    print(_ids_to_df(b_only_ids))

    print("\n#################### BETTER IN A: ####################")
    print(_ids_to_df(better_a_ids))

    print("\n#################### BETTER IN B: ####################")
    print(_ids_to_df(better_b_ids))


if __name__ == "__main__":
    _main()
