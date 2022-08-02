"""Command line flags."""

import argparse

FLAGS = argparse.Namespace()  # set by parse_flags() below


def parse_flags() -> None:
    """Parse the command line flags and update global FLAGS."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True, type=str)
    parser.add_argument("--approach", required=True, type=str)
    parser.add_argument("--num_train_tasks", default=5, type=int)
    parser.add_argument("--num_eval_tasks", default=10, type=int)
    args = parser.parse_args()
    FLAGS.__dict__.update(args.__dict__)
