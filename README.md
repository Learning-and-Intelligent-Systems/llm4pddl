# llm4pddl

Under development.

### `PYTHONHASHSEED`

Our code assumes that python hashing is deterministic between processes, which is [not true by default](https://stackoverflow.com/questions/30585108/disable-hash-randomization-from-within-python-program).
Please make sure to `export PYTHONHASHSEED=0` when running the code. You can add this line to your bash/zsh profile, or prepend `export PYTHONHASHSEED=0` to any command line call, e.g., `export PYTHONHASHSEED=0 python llm4pddl/main.py --env ...`.

## Requirements

- Python 3.8+
- Tested on MacOS Catalina and Ubuntu 18.04

## Instructions For Contributing

- (Highly recommended) Make a virtual environment:
  - `virtualenv venv`
  - `source venv/bin/activate`
- Clone this repository with submodules: `git clone --recursive https://github.com/Learning-and-Intelligent-Systems/llm4pddl.git`
- Run `pip install -e .[develop]` to install the main dependencies for development.
  - If you encounter issues with the `transformers` dependency on MacOS, we recommend doing the following:
    1. Run `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` in terminal.
    2. Restart the terminal.
    3. Run `pip install transformers==2.5.1`.
  - If problems persist, see https://github.com/huggingface/transformers/issues/2831.
- Run `pip install -e llm4pddl/third_party/pyperplan` to install our fork of pyperplan.
- You can't push directly to master. Make a new branch in this repository (don't use a fork, since that will not properly trigger the checks when you make a PR). When your code is ready for review, make a PR and request reviews from the appropriate people.
- To merge a PR, you need at least one approval, and you have to pass the 4 checks defined in `.github/workflows/llm4pddl.yml`, which you can run locally as follows:
  - `pytest -s tests/ --cov-config=.coveragerc --cov=llm4pddl/ --cov=tests/ --cov-fail-under=100 --cov-report=term-missing:skip-covered --durations=0`
  - `mypy .`
  - `pytest . --pylint -m pylint --pylint-rcfile=.llm4pddl_pylintrc`
  - `./run_autoformat.sh`
- The first one is the unit testing check, which verifies that unit tests pass and that code is adequately covered. The "100" means that all lines in every file must be covered.
- The second one is the static typing check, which uses Mypy to verify type annotations.
- The third one is the linter check, which runs Pylint with the custom config file `.llm4pddl_pylintrc` in the root of this repository. Feel free to edit this file as necessary.
- The fourth one is the autoformatting check, which uses the custom config files `.style.yapf` and `.isort.cfg` in the root of this repository.
