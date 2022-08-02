"""Main script for running experiments."""

from llm4pddl.flags import FLAGS, parse_flags


def _main() -> None:
    """The main entry point."""
    parse_flags()
    env = FLAGS.env
    approach = FLAGS.approach
    print("Env:", env)
    print("Approach:", approach)


if __name__ == "__main__":  # pragma: no cover
    _main()
