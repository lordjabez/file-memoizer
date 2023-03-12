#!/usr/bin/env bash
set -e

poetry run pytest -vv --cov=file_memoizer --cov-report=term --cov-report=xml --cov-fail-under=95 $@
