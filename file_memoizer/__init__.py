"""File Memoizer main module"""

__version__ = '0.0.0'


import datetime
import hashlib
import json
import os
import pathlib

import cachier


_default_cache_directory = os.path.join(pathlib.Path.home(), '.file-memoizer', 'default')
_default_cache_ttl = datetime.timedelta(days=1)


def _get_cache_key_ignoring_unhashable(*args):
    """
    Get a cache key by producing a JSON string of the arguments then applying SHA256.

    :param args: List of function arguments to hash
    """
    args_hash = hashlib.sha256()
    key = json.dumps(list(args), default=lambda d: '', sort_keys=True)
    args_hash.update(key.encode())
    return args_hash.hexdigest()


def memoize(cache_directory=None, cache_ttl=None, unhashable_args='fail'):
    """
    Get a memoization annotation function.

    :param cache_directory: Location to store cache files; defaults to a subfolder of home
    :param cache_ttl: Time delta object of duration to keep cache files; defaults to a day
    :param unhashable_args: Determine what to do with any unhashable args, either 'ignore' or 'fail' (the default)
    """
    cache_params = {'separate_files': True}
    cache_params['cache_dir'] = cache_directory or _default_cache_directory
    cache_params['stale_after'] = cache_ttl or _default_cache_ttl
    if unhashable_args == 'ignore':
        cache_params['hash_params'] = _get_cache_key_ignoring_unhashable
    return cachier.cachier(**cache_params)
