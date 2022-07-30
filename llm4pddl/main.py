"""Main script for running experiments."""

from typing import Sequence

from absl import app

from llm4pddl.flags import FLAGS


def _main(argv: Sequence[str]) -> None:
    assert len(argv) == 1  # just the name of this file
    domain = FLAGS.domain
    approach = FLAGS.approach
    print("Domain:", domain)
    print("Approach:", approach)


if __name__ == "__main__":
    app.run(_main)
