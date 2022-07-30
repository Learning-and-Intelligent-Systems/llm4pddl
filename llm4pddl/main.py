"""Main script for running experiments."""

from absl import app
from typing import Sequence

from llm4pddl.flags import FLAGS


def _main(argv: Sequence[str]) -> None:
    assert len(argv) == 1  # just the name of this file
    

if __name__ == "__main__":
    app.run(_main)
