# CSVW DuckDB tool

Convert a [CSVW document](https://csvw.org/) (CSV metadata) to a [DuckDB](https://duckdb.org/) query to load a CSV file into a
database.

See also: Python [csvw package](https://github.com/cldf/csvw).

# Installation

```bash
pip install csvw-duckdb
```

# Usage

```bash
csvw-duckdb --help
```
```
usage: csvw-duckdb [-h] [--version] csvw_path

Load a CSVW document and generate simple SQL SELECT statements. One SQL file will be generated per table in the CSVW table group.

positional arguments:
  csvw_path   CSVW file

options:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

## Examples

```bash
csvw-duckdb my_metadata.csvw
```
