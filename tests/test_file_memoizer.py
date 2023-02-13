"""TODO."""


import toml

import file_memoizer


with open('pyproject.toml', encoding='utf-8') as project_file:
    project = toml.load(project_file)


def test_version():
    """Package version number is populated as expected."""
    version = project['tool']['poetry']['version']
    assert file_memoizer.__version__ == version
