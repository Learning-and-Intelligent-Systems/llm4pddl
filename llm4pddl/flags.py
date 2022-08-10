"""Command line flags."""

import argparse
import logging

FLAGS = argparse.Namespace()  # set by parse_flags() below


def parse_flags() -> None:
    """Parse the command line flags and update global FLAGS."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True, type=str)
    parser.add_argument("--approach", required=True, type=str)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--experiment_id", default="", type=str)
    parser.add_argument("--num_train_tasks", default=5, type=int)
    parser.add_argument("--num_eval_tasks", default=10, type=int)
    parser.add_argument("--planner", default="pyperplan", type=str)
    parser.add_argument("--data_gen_planner", default="fastdownward", type=str)
    parser.add_argument("--planning_timeout", default=100.0, type=float)
    parser.add_argument("--results_dir", default="results", type=str)
    parser.add_argument("--llm_cache_dir", default="llm_cache", type=str)
    parser.add_argument("--llm_use_cache_only", action="store_true")
    # Also try: "text-davinci-002"
    parser.add_argument("--llm_model_name", default="code-davinci-002")
    # Note that this temperature is only used by the multi LLM approaches,
    # not by the standard (single response) approach, which always uses 0.0.
    parser.add_argument("--llm_multi_temperature", default=0.5, type=float)
    # Note that this num_completions is only used by the multi LLM approaches,
    # not by the standard (single response) approach, which always uses 1.
    parser.add_argument("--llm_multi_num_completions", default=5, type=int)
    parser.add_argument("--llm_max_total_tokens", default=4096, type=int)
    parser.add_argument('--debug',
                        action="store_const",
                        dest="loglevel",
                        const=logging.DEBUG,
                        default=logging.INFO)
    args = parser.parse_args()
    FLAGS.__dict__.update(args.__dict__)
