# winzy-head-tail

[![PyPI](https://img.shields.io/pypi/v/winzy-head-tail.svg)](https://pypi.org/project/winzy-head-tail/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-head-tail?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-head-tail/releases)
[![Tests](https://github.com/sukhbinder/winzy-head-tail/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-head-tail/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-head-tail/blob/main/LICENSE)

Mimics head and tail command using python

## Installation

First [install winzy](https://github.com/sukhbinder/winzy) by typing

```bash
pip install winzy
```

Then install this plugin in the same environment as your Winzy application.
```bash
winzy install winzy-head-tail
```
## Usage

For head

```bash
usage: winzy head [-h] [-n N] [-c C] [FILE ...]

Mimics head command using python

positional arguments:
  FILE        File(s) to process. Reads from stdin if none provided.

optional arguments:
  -h, --help  show this help message and exit
  -n N        Number of lines to display (default: 10).
  -c C        Number of bytes to display (overrides -n).


```

For Tail

```bash
usage: winzy tail [-h] [-n N] [-c C] [FILE ...]

Mimics tail command using python

positional arguments:
  FILE        File(s) to process. Reads from stdin if none provided.

optional arguments:
  -h, --help  show this help message and exit
  -n N        Number of lines to display (default: 10).
  -c C        Number of bytes to display (overrides -n).


```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-head-tail
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
