import csvw.db


class Table:
    def __init__(self, table_spec: csvw.db.TableSpec):
        self.table_spec = table_spec

    def sql(self, *args, **kwargs):
        """
        Convert SQLite SQL to DuckDB SQL syntax.
        https://www.sqlite.org/lang.html
        https://duckdb.org/docs/sql/introduction
        """
        sql = self.table_spec.sql(*args, **kwargs)
        sql += ";"
        sql = sql.replace("`", '"')
        return sql
