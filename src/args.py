"""Contains settings that vary per run."""
import argparse

def create_arg_parser() -> argparse.ArgumentParser:
    """Defines command line argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True, type=str)
    parser.add_argument("--approach", required=True, type=str)
    parser.add_argument("--seed", required=True, type=int)
    return parser
