# gitfiles

[![PyPI](https://img.shields.io/pypi/v/gitfiles)](https://pypi.org/project/gitfiles/)
[![Python](https://img.shields.io/pypi/pyversions/gitfiles)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/gitfiles)
![Status](https://img.shields.io/pypi/status/gitfiles)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/legopitstop/gitfiles)](https://github.com/legopitstop/gitfiles/issues)

Load, filter and match `.gitingore` files.

## Installation

Install the module with pip:

```bat
pip3 install gitfiles
```

Update existing installation: `pip3 install gitfiles --upgrade`

## Examples

```Python
import gitfiles

print(gitfiles.match('file.so'))
```

```Python
import gitfiles

files = [
    '.venv',
    '.env',
    'app.py'
]
print(gitfiles.filter(files))
```
