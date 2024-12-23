# smartchg

[![GitHub main workflow](https://img.shields.io/github/actions/workflow/status/dmotte/smartchg/main.yml?branch=main&logo=github&label=main&style=flat-square)](https://github.com/dmotte/smartchg/actions)
[![PyPI](https://img.shields.io/pypi/v/smartchg?logo=python&style=flat-square)](https://pypi.org/project/smartchg/)

:snake: DCA-based asset **exchange algorithm**.

## Installation

This utility is available as a Python package on **PyPI**:

```bash
pip3 install smartchg
```

## Usage

There are some files in the [`example`](example) directory of this repo that can be useful to demonstrate how this tool works, so let's change directory first:

```bash
cd example/
```

We need a Python **virtual environment** ("venv") with some packages to do the demonstration:

```bash
python3 -mvenv venv
venv/bin/python3 -mpip install -r requirements.txt
```

Now we need to **fetch data** related to some asset. To do that, we can use https://github.com/dmotte/misc/blob/main/python-scripts/ohlcv-fetchers/yahoo-finance.py.

TODO if needed (please check), note here that more than 1 year of data is needed

> **Note**: in the following commands, replace the local path of the `invoke.sh` script with the correct one.

```bash
~/git/misc/python-scripts/ohlcv-fetchers/invoke.sh yahoo-finance '^GSPC' -i1d -d2020-01-01T00Z -f'{:.6f}' > ohlcv-SPX500.csv
```

TODO complete this part. You can take inspiration from apycalc

For more details on how to use this command, you can also refer to its help message (`--help`).

## Development

If you want to contribute to this project, you can install the package in **editable** mode:

```bash
pip3 install -e . --user
```

This will just link the package to the original location, basically meaning any changes to the original package would reflect directly in your environment ([source](https://stackoverflow.com/a/35064498)).

If you want to run the tests, you'll have to install the `pytest` package and then run:

```bash
pytest test
```
