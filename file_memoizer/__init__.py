"""File Memoizer main module"""

__version__ = '0.0.0'


import datetime
import functools
import hashlib
import inspect
import json
import os
import pathlib

import cachier


_default_cache_directory = os.path.join(pathlib.Path.home(), '.file-memoizer')
_default_cache_ttl = datetime.timedelta(days=1)


def _get_cache_key(args, kwargs, ignore_unhashable=False):
    """
    Get a cache key by producing a JSON string of the arguments then applying SHA256.

    :param args: List of function arguments to hash
    """
    args_list = [a for a in args] + [k for k in kwargs.items() if k[0] != 'result_to_cache']
    if ignore_unhashable:
        key = json.dumps(args_list, default=lambda d: '', sort_keys=True)
    else:
        key = json.dumps(args_list, sort_keys=True)
    args_hash = hashlib.sha256()
    args_hash.update(key.encode())
    return args_hash.hexdigest()


def memoize(cache_ttl=None, cache_directory=None, unhashable_args='fail'):
    """
    Get a memoization annotation function.

    :param cache_ttl: Time delta object of duration to keep cache files; defaults to a day
    :param cache_directory: Location to store cache files; defaults to a subfolder of home
    :param unhashable_args: Determine what to do with any unhashable args, either 'ignore' or 'fail' (the default)
    """

    cache_params = {'separate_files': True}
    cache_params['stale_after'] = cache_ttl or _default_cache_ttl
    if cache_directory is None:
        calling_module_name = inspect.getmodule(inspect.stack()[1][0]).__name__
        cache_params['cache_dir'] = os.path.join(_default_cache_directory, calling_module_name)
    else:
        cache_params['cache_dir'] = cache_directory
    if unhashable_args == 'ignore':
        cache_params['hash_params'] = functools.partial(_get_cache_key, ignore_unhashable=True)
    else:
        cache_params['hash_params'] = _get_cache_key

    def decorator(function_to_memoize):
        @cachier.cachier(**cache_params)
        @functools.wraps(function_to_memoize)
        def wrapper(*args, **kwargs):
            return kwargs['result_to_cache'] if 'result_to_cache' in kwargs else function_to_memoize(*args, **kwargs)
        wrapper.precache_result = functools.partial(wrapper, overwrite_cache=True)
        return wrapper

    return decorator
