"""File Memoizer test module"""


import datetime
import os
import shutil
import tempfile
import toml

import file_memoizer


with open('pyproject.toml', encoding='utf-8') as project_file:
    project = toml.load(project_file)


_temp_directory = os.path.join(tempfile.gettempdir(), 'file-memoizer-test')
_execution_flag_filename = os.path.join(_temp_directory, 'execution-flag')


shutil.rmtree(file_memoizer._default_cache_directory, ignore_errors=True)  # pylint: disable=protected-access
shutil.rmtree(_temp_directory, ignore_errors=True)


def _set_execution_flag():
    os.makedirs(_temp_directory, exist_ok=True)
    with open(_execution_flag_filename, 'w', encoding='utf-8') as execution_file:
        execution_file.write('executed')


def _clear_execution_flag():
    try:
        os.remove(_execution_flag_filename)
    except FileNotFoundError:
        pass


def _execution_flag_exists():
    return os.path.isfile(_execution_flag_filename)


def test_version():
    """Package version number is populated as expected."""
    version = project['tool']['poetry']['version']
    assert file_memoizer.__version__ == version


def test_default_memoize():
    """Default memoize annotation works as expected."""
    _clear_execution_flag()

    @file_memoizer.memoize()
    def double(value):
        _set_execution_flag()
        return value * 2
    result = double(1)
    assert result == 2
    assert _execution_flag_exists()
    _clear_execution_flag()
    result = double(1)
    assert result == 2
    assert not _execution_flag_exists()


def test_custom_memoize():
    """Customized memoize annotation works as expected."""
    _clear_execution_flag()

    cache_directory = _temp_directory
    cache_ttl = datetime.timedelta(seconds=1)

    @file_memoizer.memoize(cache_directory, cache_ttl, 'ignore')
    def double(value):
        _set_execution_flag()
        return value * 2
    result = double(1)
    assert result == 2
    assert _execution_flag_exists()
    _clear_execution_flag()
    result = double(1)
    assert result == 2
    assert not _execution_flag_exists()
