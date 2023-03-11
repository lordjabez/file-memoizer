"""File Memoizer code quality test module"""


import subprocess  # nosec B404


def test_flake8():
    """Flake8 linter passes with no warnings or errors."""
    command = ('poetry', 'run', 'flake8')
    parameters = ('--max-line-length=120', '--statistics', 'file_memoizer')
    subprocess.check_call(command + parameters)  # nosec B603
    parameters = ('--max-line-length=120', '--statistics', 'tests')
    subprocess.check_call(command + parameters)  # nosec B603
