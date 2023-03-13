"""File Memoizer code quality test module"""


import subprocess  # nosec B404


def test_flake8():
    """Flake8 linter passes with no warnings or errors."""
    command = ('poetry', 'run', 'flake8')
    parameters = ('--max-line-length=120', '--statistics', 'file_memoizer', 'tests')
    subprocess.check_call(command + parameters)  # nosec B603


def test_pylint():
    """Pylint linter passes with no warnings or errors."""
    command = ('poetry', 'run', 'pylint')
    parameters = ('--max-line-length=120', 'file_memoizer', 'tests')
    subprocess.check_call(command + parameters)  # nosec B603
