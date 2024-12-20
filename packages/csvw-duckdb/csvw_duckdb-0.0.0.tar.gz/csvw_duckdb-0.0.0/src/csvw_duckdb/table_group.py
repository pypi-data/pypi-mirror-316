import csvw.db
import csvw_duckdb.table


class TableGroup:
    """
    A group of tables, which are data structure made of a collection of rows and columns.
    https://www.w3.org/ns/csvw#class-definitions
    """

    def __init__(self, path):
        """
        :param table: CSVW table definition https://www.w3.org/ns/csvw#class-definitions
        """
        self.path = path
        self.table_group = csvw.TableGroup.from_file(path)
        self.database = csvw.db.Database(self.table_group)
        "SQLite database"

    @property
    def tables(self):
        for table in self.database.tables:
            yield csvw_duckdb.table.Table(table)

    def iter_sql(self):
        """
        Get the SQL CREATE TABLE statement for each table in the database.
        """
        # https://csvw.readthedocs.io/en/latest/db.html
        for table in self.tables:
            yield table.sql(translate=self.database.translate)
