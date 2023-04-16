"""File Memoizer test module"""


import datetime
import os
import shutil
import tempfile
import time
import toml

import file_memoizer


with open('pyproject.toml', encoding='utf-8') as project_file:
    project = toml.load(project_file)


_execution_flag_directory = tempfile.gettempdir()
_execution_flag_filename = os.path.join(_execution_flag_directory, 'execution-flag')

_default_cache_directory = file_memoizer._default_cache_directory  # pylint: disable=protected-access
_custom_cache_directory = os.path.join(tempfile.gettempdir(), 'file-memoizer-test')

_custom_cache_ttl = datetime.timedelta(seconds=1)


def _clear_default_cache():
    shutil.rmtree(_default_cache_directory, ignore_errors=True)


def _clear_custom_cache():
    shutil.rmtree(_custom_cache_directory, ignore_errors=True)


def _set_execution_flag():
    os.makedirs(_execution_flag_directory, exist_ok=True)
    with open(_execution_flag_filename, 'w', encoding='utf-8') as execution_file:
        execution_file.write('executed')


def _clear_execution_flag():
    try:
        os.remove(_execution_flag_filename)
    except FileNotFoundError:
        pass


def _execution_flag_exists():
    return os.path.isfile(_execution_flag_filename)


def setup():
    """Clear all storage before every test."""
    _clear_default_cache()
    _clear_custom_cache()
    _clear_execution_flag()


def test_version():
    """Package version number is populated as expected."""
    version = project['tool']['poetry']['version']
    assert file_memoizer.__version__ == version


def test_default_memoize():
    """Default memoize annotation works as expected."""

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
    _clear_execution_flag()
    double.clear_cache()  # pylint: disable=no-member

    result = double(1)
    assert result == 2
    assert _execution_flag_exists()


def test_custom_ttl():
    """Customized cache time-to-live is used when provided."""

    @file_memoizer.memoize(cache_ttl=_custom_cache_ttl)
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
    _clear_execution_flag()
    time.sleep(2)

    result = double(1)
    assert result == 2
    assert _execution_flag_exists()


def test_custom_directory():
    """Customized cache file location is used when provided."""

    @file_memoizer.memoize(cache_directory=_custom_cache_directory)
    def double(value):
        _set_execution_flag()
        return value * 2

    assert double.cache_dpath() == _custom_cache_directory


def test_static_method():
    """Static class method caches as expected."""

    class TestClass():  # pylint: disable=missing-class-docstring,too-few-public-methods
        @staticmethod
        @file_memoizer.memoize()
        def triple(value):  # pylint: disable=missing-function-docstring
            _set_execution_flag()
            return value * 3

    result = TestClass.triple(1)
    assert result == 3
    assert _execution_flag_exists()
    _clear_execution_flag()

    result = TestClass.triple(1)
    assert result == 3
    assert not _execution_flag_exists()
    _clear_execution_flag()
    TestClass.triple.clear_cache()  # pylint: disable=no-member

    result = TestClass.triple(1)
    assert result == 3
    assert _execution_flag_exists()


def test_object_method():
    """Object method caches as expected."""

    class TestClass():  # pylint: disable=missing-class-docstring,too-few-public-methods
        @file_memoizer.memoize()
        def triple(self, value):  # pylint: disable=missing-function-docstring
            _set_execution_flag()
            return value * 3

    result = TestClass().triple(1)
    assert result == 3
    assert _execution_flag_exists()
    _clear_execution_flag()

    result = TestClass().triple(1)
    assert result == 3
    assert not _execution_flag_exists()
    _clear_execution_flag()
    TestClass.triple.clear_cache()  # pylint: disable=no-member

    result = TestClass().triple(1)
    assert result == 3
    assert _execution_flag_exists()


def test_precache_value():
    """Precached value is returned when provided."""

    class TestClass():  # pylint: disable=missing-class-docstring,too-few-public-methods
        @file_memoizer.memoize()
        def multiply(self, value_1, value_2):  # pylint: disable=missing-function-docstring
            return value_1 * value_2

    @file_memoizer.memoize()
    def multiply(value_1, value_2):
        return value_1 * value_2

    multiply.precache_value(2, 3, value_to_cache=7)  # pylint: disable=no-member
    result = multiply(2, 3)
    assert result == 7

    TestClass().multiply.precache_value(2, 3, value_to_cache=8)  # pylint: disable=no-member
    result = TestClass().multiply(2, 3)
    assert result == 8
    TestClass().multiply.clear_cache()  # pylint: disable=no-member
    result = TestClass().multiply(2, 3)
    assert result == 6

    result = multiply(2, 3)
    assert result == 7
    multiply.clear_cache()
    result = multiply(2, 3)
    assert result == 6
