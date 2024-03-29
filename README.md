# File Memoizer

[![license](https://img.shields.io/github/license/lordjabez/file-memoizer?color=blue&label=License)](https://opensource.org/licenses/MIT)
[![PyPi:version](https://img.shields.io/pypi/v/file-memoizer?color=blue&label=PyPI)](https://pypi.org/project/file-memoizer/)
[![Tests](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml)
[![Release](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml)

NOTICE: This package is deprecated and will no longer be updated, as the functionality it provides
has now been inplemented directly in [cachier](https://github.com/python-cachier/cachier). Please
use that package directly.


## Installation

Installation is via `pip`:

```bash
pip install file-memoizer
```


## Usage

To cache a function's value, annotate it by calling the `memoize`
function as follows. Note that all function arguments must be hashable
for it to be cached else a TypeError will be thrown.

```python
import file_memoizer

@file_memoizer.memoize()
def double(n):
    return 2 * n
```

By default the cached values remain valid for a day. This can be changed
with the `cache_ttl` parameter:

```python
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

```python
import datetime
import file_memoizer

custom_path = '/path/to/store/files'

@file_memoizer.memoize(cache_directory=custom_path)
def quadruple(n):
    return 4 * n
```

The memoizer will automatically ignore a function's first parameter if named self,
so that instance methods can be cached. It is the caller's responsibility to ensure
the result of the method does not depend on the state of the object's internals.
This is most useful when the object is being used to call an external service.

```python
import requests

class ExampleAPIClient():

    @file_memoizer.memoize()
    def get(self, url):
        return self.session.get(url)

    def __init__(self):
        self.session = requests.Session()
```
