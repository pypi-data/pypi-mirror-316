[![Test Python code](https://github.com/CUREd-Plus/csvw-duckdb/actions/workflows/test.yaml/badge.svg)](https://github.com/CUREd-Plus/csvw-duckdb/actions/workflows/test.yaml)

# CSVW DuckDB tool

Convert a [CSVW document](https://csvw.org/) (CSV metadata) to a [DuckDB](https://duckdb.org/) query to load a CSV file into a
database.

See also: Python [csvw package](https://github.com/cldf/csvw).

# Installation

```bash
pip install csvw-duckdb
```

# Usage

To use this tool, call it from the command line and provide the path of the CSVW document.
The SQL code will be written to the screen.

```bash
csvw-duckdb --help
```
```
usage: csvw-duckdb [-h] [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--version] csvw_path

Load a CSVW document and generate simple SQL SELECT statements. One SQL file will be generated per table in the CSVW table group.

positional arguments:
  csvw_path             CSVW file

options:
  -h, --help            show this help message and exit
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}, -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}
  --version             show program's version number and exi
```

## Examples

```bash
csvw-duckdb my_metadata.csvw
```
