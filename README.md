# File Memoizer

[![license](https://img.shields.io/github/license/lordjabez/file-memoizer?color=blue&label=License)](https://opensource.org/licenses/MIT)
[![PyPi:version](https://img.shields.io/pypi/v/file-memoizer?color=blue&label=PyPI)](https://pypi.org/project/file-memoizer/)
[![Tests](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml)
[![Linter](https://github.com/lordjabez/file-memoizer/actions/workflows/lint.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/lint.yml)
[![Security](https://github.com/lordjabez/file-memoizer/actions/workflows/scan.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/scan.yml)
[![Release](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml)

This Python package makes it easy to store function results across executions using cache files.


## Prerequisites

Installation is via `pip`:

```bash
pip install file-memoizer
```


## Usage

Basic usage is as follows:

```python3
import file_memoizer

file_memoizer.memoize()
def double(n):
    return 2 * n

class Arithmetic():

    @staticmethod
    @file_memoizer.memoize()
    def triple(n):
         return 3 * n
    
    @file_memoizer.memoize()
    def multiply(self, x, y):
        return x * y
```
