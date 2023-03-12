#!/usr/bin/env bash
set -e

VERSION_NUMBER="$(git describe --tags --abbrev=8 | sed 's/-.*g/+/' | tr -d 'v')"
VERSION_NUMBER="${VERSION_NUMBER:-0.0.0}"

sed -i "s/version = \"0.0.0\"/version = \"${VERSION_NUMBER}\"/" pyproject.toml
sed -i "s/__version__ = '0.0.0'/__version__ = '${VERSION_NUMBER}'/" file_memoizer/__init__.py
