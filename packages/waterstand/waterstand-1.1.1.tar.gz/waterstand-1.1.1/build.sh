#!/bin/bash
set -e
export PYTHONPATH=.
python3 -m pip install --upgrade build
pip install -r requirements.txt
pip list --outdated
pylint *.py
coverage run -m pytest
coverage report -m
rm dist/*
python -m build
