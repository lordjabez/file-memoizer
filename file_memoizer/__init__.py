"""File Memoizer main module"""

__version__ = '0.0.0'


import datetime
import inspect
import os
import pathlib
import warnings

import cachier


warnings.warn('This package is deprecated; use cachier directly instead.', DeprecationWarning)


_default_cache_directory = os.path.join(pathlib.Path.home(), '.file-memoizer')
_default_cache_ttl = datetime.timedelta(days=1)


def memoize(cache_ttl=None, cache_directory=None):
    """
    Get a memoization annotation function.

    :param cache_ttl: Time delta object of duration to keep cache files; defaults to a day
    :param cache_directory: Location to store cache files; defaults to a subfolder of home
    """

    cache_params = {'separate_files': True}
    cache_params['stale_after'] = cache_ttl or _default_cache_ttl
    if cache_directory is None:
        calling_module_name = inspect.getmodule(inspect.stack()[1][0]).__name__
        cache_params['cache_dir'] = os.path.join(_default_cache_directory, calling_module_name)
    else:
        cache_params['cache_dir'] = cache_directory

    return cachier.cachier(**cache_params)
