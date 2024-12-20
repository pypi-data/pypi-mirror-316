import logging

import duckdb
from csvw_duckdb.table_group import TableGroup

logger = logging.getLogger(__name__)


def test_duckdb():
    # https://duckdb.org/docs/api/python/overview
    tg = TableGroup("tests/data/hes_ae.json")
    con = duckdb.connect(":memory:")
    for sql in tg.iter_sql():
        try:
            con.sql(sql)
        except duckdb.ParserException:
            logger.error(sql)
            raise
