"""TODO."""

__version__ = '0.0.0'


import datetime
import functools
import hashlib
import json
import os
import pathlib

import cachier


def _get_cache_key(*args):
    """TODO."""
    args_hash = hashlib.sha256()
    key = json.dumps(list(args), default=lambda d: '', sort_keys=True)
    args_hash.update(key.encode())
    return args_hash.hexdigest()


_cache_dir = os.path.join(pathlib.Path.home(), '.file-memoizer', __name__)
_cache_ttl = datetime.timedelta(days=7)
_cache_params = {
    'cache_dir': _cache_dir,
    'hash_params': _get_cache_key,
    'stale_after': _cache_ttl,
    'separate_files': True,
}


def memoize():
    """TODO."""
    return functools.partial(cachier.cachier, **_cache_params)
