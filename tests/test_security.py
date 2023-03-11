"""File Memoizer security test module"""


import subprocess  # nosec B404


def test_bandit():
    """Bandit security scan passes with no warnings or errors."""
    command = ('poetry', 'run', 'bandit')
    parameters = ('-r', 'file_memoizer')
    subprocess.check_call(command + parameters)  # nosec B603
    parameters = ('-s', 'B101', '-r', 'tests')
    subprocess.check_call(command + parameters)  # nosec B603


def test_safety():
    """Bandit security scan passes with no warnings or errors."""
    command = ('poetry', 'run', 'safety')
    parameters = ('check', '--full-report')
    subprocess.check_call(command + parameters)  # nosec B603
