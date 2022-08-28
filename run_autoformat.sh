#!/bin/bash
yapf -i -r --style .style.yapf --exclude '**/third_party' llm4pddl
yapf -i -r --style .style.yapf scripts
yapf -i -r --style .style.yapf tests
yapf -i -r --style .style.yapf *.py
docformatter -i -r . --exclude venv llm4pddl/third_party
isort .
