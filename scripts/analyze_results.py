"""Create a table summarizing results saved to a directory."""

import argparse
import functools
import glob
import pickle
from pathlib import Path
from typing import Any, Callable, Dict, Set, Tuple

import numpy as np
import pandas as pd

from llm4pddl.structs import TaskMetrics


def _get_approach_id(metrics: TaskMetrics) -> str:
    if "experiment_id" in metrics and "-" in metrics["experiment_id"]:
        return metrics["experiment_id"].split("-", 1)[1]
    return "no-id-" + metrics["approach"]


@functools.lru_cache(maxsize=None)
def _get_success_task_ids(results_dir: str) -> Set[str]:
    initial_derived_cols = _create_derived_cols(results_dir,
                                                include_success_metrics=False)
    raw_results = _load_results(results_dir, derived_cols=initial_derived_cols)
    all_task_ids = set(raw_results.task_id)
    # Tasks where at least one approach failed.
    some_failed_task_ids = set(raw_results[raw_results.success < 1].task_id)
    # Tasks where all approaches succeeded.
    all_succeeded_task_ids = all_task_ids - some_failed_task_ids
    return all_succeeded_task_ids


def _create_success_metric(results_dir: str,
                           metric_name: str) -> Callable[[TaskMetrics], Any]:
    success_task_ids = _get_success_task_ids(results_dir)

    def _get_success_metric(metrics: TaskMetrics) -> float:
        if metrics["task_id"] not in success_task_ids:
            return 0.0  # default to 0
        return metrics[metric_name]

    return _get_success_metric


def _create_derived_cols(
    results_dir: str,
    include_success_metrics: bool = True
) -> Dict[str, Callable[[TaskMetrics], Any]]:
    derived_cols = {
        "success": lambda d: float(d["result"] == "success"),
        "approach_id": _get_approach_id,
    }
    if include_success_metrics:
        derived_cols["success_nodes_created"] = _create_success_metric(
            results_dir, "nodes_created")
        derived_cols["success_nodes_expanded"] = _create_success_metric(
            results_dir, "nodes_expanded")
    return derived_cols


def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results_dir", default="results", type=str)
    parser.add_argument("--a_dir", type=str)
    parser.add_argument("--b_dir", type=str)
    args = parser.parse_args()
    if args.a_dir:
        assert args.b_dir
        a_derived_cols = _create_derived_cols(args.a_dir)
        a_results = _load_results(args.a_dir, derived_cols=a_derived_cols)
        a_summary = _create_summary_table(a_results,
                                          verbose=False,
                                          save_summary=False)
        b_derived_cols = _create_derived_cols(args.b_dir)
        b_results = _load_results(args.b_dir, derived_cols=b_derived_cols)
        b_summary = _create_summary_table(b_results,
                                          verbose=False,
                                          save_summary=False)
        _summarize_diff(a_summary, b_summary)
    else:
        derived_cols = _create_derived_cols(args.results_dir)
        results = _load_results(args.results_dir, derived_cols)
        _create_summary_table(results)


def _load_results(
    results_dir: str,
    derived_cols: Dict[str, Callable[[TaskMetrics], Any]],
) -> pd.DataFrame:
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
            for col, derive_fn in derived_cols.items():
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
    # Change names to be more concise and capitalizing them
    for name in raw_results['env']:
        if name.startswith('pyperplan-'):
            if name == 'pyperplan-tpp':
                raw_results['env'] = raw_results['env'].replace([name], 'TPP')
            else:
                raw_results['env'] = raw_results['env'].replace(
                    [name], name[10].upper() + name[11:])
        elif name.startswith('custom-'):
            raw_results['env'] = raw_results['env'].replace(
                [name], name[7].upper() + name[8:])
    # Remove the non-numeric columns that we don't need anymore.
    df = raw_results.drop(columns=["result"])
    # Group by env, approach, seed, and experiment ID.
    grouped = df.groupby(["env", "approach_id", "seed", "experiment_id"])
    # Average over eval tasks.
    eval_means = grouped.mean().reset_index()
    # Get statistics over seed.
    grouped = eval_means.groupby(["env", "approach_id", "experiment_id"])
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
        summary = summary.reset_index()
        envs = summary.env.unique()
        metrics = [
            "success_nodes_created", "success_nodes_expanded", "success",
            "num_seeds"
        ]
        # env -> approach X metric -> value
        reshaped_data: Dict[str, Dict[Tuple[str, str],
                                      float]] = {env: {}
                                                 for env in envs}
        for _, row in summary.iterrows():
            for metric in metrics:
                reshaped_data[row.env][(row.approach_id, metric)] = row[metric]
        summary_nested = pd.DataFrame(reshaped_data).transpose()
        # Report the total number of results.
        print(f"\nTOTAL RESULTS: {df.shape[0]}")
        # Create an even higher-level summary, averaging over everything except
        # the approach.
        print("\nSUMMARY OF THE SUMMARY:")
        print(df.groupby(["approach_id"]).mean())
    if save_summary:
        summary_nested.to_csv("results_summary.csv")
        print("\n\nWrote out table to results_summary.csv")
    # Removing num_seeds from chart
    summary_nested = summary_nested.drop('num_seeds', axis=1, level=1)
    # Adding Averages row
    avgs = []
    avgs_std = []
    for col in summary_nested:
        SUM = 0.0
        SUM_std = 0.0
        number = 0.0
        for num_str in summary_nested[col]:
            num_str = num_str.replace(')', '')
            num_str = num_str.replace('(', '')
            numbers = num_str.split(' ')
            num, num_std = numbers
            SUM += float(num)
            SUM_std += float(num_std)
            number += 1.0
        avg = round(SUM / number, 3)
        avg_std = round(SUM_std / number, 3)
        avgs.append(avg)
        avgs_std.append(avg_std)
        full_strings = [
            f'{avg_} ({avg_std_})' for avg_, avg_std_ in zip(avgs, avgs_std)
        ]
    summary_nested.loc['Average'] = full_strings

    # Changing names
    summary_nested = summary_nested.rename(
        columns={
            'success_nodes_created': 'created',
            'success_nodes_expanded': 'expanded',
            'llm-standard': 'LLM Standard',
            'llm-standard-plan': 'LLM Standard Plan',
            'llm-standard-random-plan': 'LLM Standard Random Plan',
            'llm-standard-no-autoregress': 'No Autoregress',
            'llm-standard-no-autoregress-plan': 'No Autoregress Plan',
            'random-actions': 'Random',
            'pyperplan-only': 'Pure Planning',
            'fd-only': 'Fast Downward'
        })
    # Printing planning appendix graphs
    for col in summary_nested:
        upper_string = col[0]
        if upper_string == 'Fast Downward':
            for graph in [
                    'LLM Standard Plan', 'LLM Standard Random Plan',
                    'Pure Planning', 'Fast Downward', 'No Autoregress Plan'
            ]:
                latex = _latex_formatting(summary_nested[graph].to_latex())
                intermediate = latex.split('\n')
                add_string = '{} & \\multicolumn{3}{c}{' + graph + '} \\\\\n\\cmidrule(lr){2-4}'
                intermediate = intermediate[0:2] + [add_string
                                                    ] + intermediate[2:]
                latex = '\n'.join(intermediate)
                print(f'appendix planning graph for {graph}:\n\n{latex}\n')
            break

    # Removing created and expanded for open loop
    for col in summary_nested:
        upper_string = col[0]
        if upper_string == 'LLM Standard':
            summary_nested = summary_nested.drop(
                columns=['created', 'expanded'], level=1)
    # Printing open loop appendix graph
    for col in summary_nested:
        upper_string = col[0]
        if upper_string == 'LLM Standard':
            latex = summary_nested.to_latex()
            latex = _latex_formatting(latex)
            print(f'appendix open loop graph:\n\n{latex}\n')
    # Removing standard deviation
    for col in summary_nested:
        for key in summary_nested[col].keys():
            summary_nested[col][key] = summary_nested[col][key].split(
                '(')[0].strip()
    # Removing fd-only and no-autoregress for planning
    for col in summary_nested:
        upper_string = col[0]
        if upper_string == 'Fast Downward':
            summary_nested = summary_nested.drop(columns=['Fast Downward'])
            summary_nested = summary_nested.drop(
                columns=['No Autoregress Plan'])
            break

    latex = summary_nested.to_latex()
    latex = _latex_formatting(latex)
    print(f'main graph:\n\n{latex}\n')
    return means.reset_index()


def _latex_formatting(latex: str) -> str:
    """input latex string, formats it the way we want."""
    # Adding horizontal line for averages
    intermediate = latex.split('\n')
    n = len(intermediate)
    latex = '\n'.join(intermediate[:n - 4] + ['\\hline \\\\ [-1.8ex]'] +
                      intermediate[n - 4:])
    # Centering labels
    if 'LLM Standard Plan' in latex:
        intermediate = latex.split('\n')
        intermediate[2] = intermediate[2].replace('{l}', '{c}', 3)
        latex = '\n'.join(intermediate)

    intermediate = latex.split('\n')
    if 'Pure Planning' in latex:
        # Adding semi lines
        intermediate = intermediate[:3] + [
            '\\cmidrule(lr){2-4} \\cmidrule(lr){5-7} \\cmidrule(lr){8-10}'
        ] + intermediate[3:]
        # Adding c
        intermediate[0] = """\\begin{tabular}{cccccccccc}"""
        latex = '\n'.join(intermediate)
    else:
        # Removing success line from open loop and adding c
        intermediate[0] = """\\begin{tabular}{cccc}"""
        latex = '\n'.join(intermediate[0:3] + intermediate[4:])

    # Bolding averages
    intermediate = latex.split('\n')
    bold_line = intermediate[-4]
    bold_line = bold_line[:-2]
    unbolded = bold_line.split('&')
    bolded = ['\\textbf{' + part + '}' for part in unbolded]
    bold_line = '&'.join(bolded)
    bold_line += '\\\\'
    intermediate[-4] = bold_line
    latex = '\n'.join(intermediate)
    return latex


def _summarize_diff(a_df: pd.DataFrame, b_df: pd.DataFrame) -> None:
    # Collect the unique (env, approach, experiment ID) in each df.
    a_ids = {(r.env, r.approach_id, r.experiment_id)
             for _, r in a_df.iterrows()}
    b_ids = {(r.env, r.approach_id, r.experiment_id)
             for _, r in b_df.iterrows()}

    # Helper to select rows from IDs.
    def _id_to_rows(df: pd.DataFrame, row_id: Tuple[str, str,
                                                    str]) -> pd.DataFrame:
        env, approach, experiment_id = row_id
        return df[((df.env == env) & (df.approach_id == approach) & \
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
