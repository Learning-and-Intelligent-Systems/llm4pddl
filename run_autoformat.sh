#!/bin/bash
yapf -i -r --style .style.yapf . --exclude venv
docformatter -i -r . --exclude venv
isort .
