"""Main script for running experiments."""

from llm4pddl.flags import FLAGS, parse_flags


def _main() -> None:
    """The main entry point."""
    parse_flags()
    domain = FLAGS.domain
    approach = FLAGS.approach
    print("Domain:", domain)
    print("Approach:", approach)


if __name__ == "__main__":  # pragma: no cover
    _main()
