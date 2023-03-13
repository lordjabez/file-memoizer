"""File Memoizer main module"""

__version__ = '0.0.0'


import datetime
import functools
import hashlib
import inspect
import os
import pathlib

import cachier


_default_cache_directory = os.path.join(pathlib.Path.home(), '.file-memoizer')
_default_cache_ttl = datetime.timedelta(days=1)


def _get_cache_key(args, kwargs, ignore_self=False):
    """
    Get a cache key hex string by using the functools make_key function.

    :param args: List of function arguments to hash
    :param kwargs: Dictionary of function keyword arguments to hash
    :param ignore_self: If true, first argument is self and should be ignored
    :return: unique hex string based on inputs
    """
    if 'result_to_cache' in kwargs:
        kwargs = {k: v for k, v in kwargs.items() if k != 'result_to_cache'}
    elif ignore_self:
        args = args[1:]
    key = functools._make_key(args, kwargs, False)  # pylint: disable=protected-access
    return hashlib.sha256(str(hash(key)).encode()).hexdigest()


def memoize(cache_ttl=None, cache_directory=None):
    """
    Get a memoization annotation function.

    :param cache_ttl: Time delta object of duration to keep cache files; defaults to a day
    :param cache_directory: Location to store cache files; defaults to a subfolder of home
    """

    def decorator(function_to_memoize):

        cache_params = {'separate_files': True}
        cache_params['stale_after'] = cache_ttl or _default_cache_ttl
        if cache_directory is None:
            calling_module_name = inspect.getmodule(inspect.stack()[1][0]).__name__
            cache_params['cache_dir'] = os.path.join(_default_cache_directory, calling_module_name)
        else:
            cache_params['cache_dir'] = cache_directory

        function_parameter_names = list(inspect.signature(function_to_memoize).parameters)
        function_is_method = function_parameter_names and function_parameter_names[0] == 'self'
        cache_params['hash_params'] = functools.partial(_get_cache_key, ignore_self=function_is_method)

        @cachier.cachier(**cache_params)
        @functools.wraps(function_to_memoize)
        def wrapper(*args, **kwargs):
            return kwargs['result_to_cache'] if 'result_to_cache' in kwargs else function_to_memoize(*args, **kwargs)
        wrapper.precache_result = functools.partial(wrapper, overwrite_cache=True)
        return wrapper

    return decorator
