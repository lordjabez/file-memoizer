# File Memoizer

[![license](https://img.shields.io/github/license/lordjabez/file-memoizer?color=blue&label=License)](https://opensource.org/licenses/MIT)
[![PyPi:version](https://img.shields.io/pypi/v/file-memoizer?color=blue&label=PyPI)](https://pypi.org/project/file-memoizer/)
[![Tests](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml)
[![Linter](https://github.com/lordjabez/file-memoizer/actions/workflows/lint.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/lint.yml)
[![Security](https://github.com/lordjabez/file-memoizer/actions/workflows/scan.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/scan.yml)
[![Release](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml)

This Python package makes it easy to store function results across executions using cache files.
Underlying functionality is provided by [cachier](https://github.com/python-cachier/cachier), but
this package adds a few conveniences, such as being able to ignore parameters that won't serialize.


## Installation

Installation is via `pip`:

```bash
pip install file-memoizer
```


## Usage

To cache a function's value, annotate it by calling the `memoize`
function as follows:

```python3
import file_memoizer

@file_memoizer.memoize()
def double(n):
    return 2 * n
```

By default the cached values remain valid for a day. This can be changed
with the `cache_ttl` parameter:

```python3
import datetime
import file_memoizer

seven_days = cache_ttl=datetime.timedelta(days=7)
@file_memoizer.memoize(cache_ttl=seven_days)
def triple(n):
    return 3 * n
```

Cache files are stored in `$HOME/.file-memoizer`, with one file per
combination of input parameters. An alternate location can be specified
with the `cache_directory` parameter:

```python3
import datetime
import file_memoizer

custom_path = '/path/to/store/files'
@file_memoizer.memoize(cache_directory=custom_path)
def quadruple(n):
    return 4 * n
```

Normally all function arguments must be hashable for it to be safely cached. However,
there are situations where it's okay to ignore them, such as an object method whose
return value doesn't depend on the object's internal state. In these cases, set
`unhashable_args='ignore'` as shown below:

class Arithmetic():

    @staticmethod
    @file_memoizer.memoize()
    def quintuple(n):
         return 5 * n
    
    @file_memoizer.memoize(unhashable_args='ignore')
    def multiply(self, x, y):
        return x * y
```
