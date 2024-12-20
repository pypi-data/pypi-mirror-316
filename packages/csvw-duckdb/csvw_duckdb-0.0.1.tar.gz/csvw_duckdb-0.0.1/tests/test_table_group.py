from csvw_duckdb.table_group import TableGroup


def test_table_group():
    tg = TableGroup("tests/data/hes_ae.json")
    for sql in tg.iter_sql():
        print(sql)
