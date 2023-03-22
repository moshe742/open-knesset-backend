from contextlib import contextmanager

import psycopg2

from . import config


def get_db_connection():
    return psycopg2.connect(
        host=config.OKNESSET_DB_HOST,
        port=config.OKNESSET_DB_PORT,
        database=config.OKNESSET_DB_NAME,
        user=config.OKNESSET_DB_USER,
        password=config.OKNESSET_DB_PASSWORD,
    )


@contextmanager
def get_db_cursor():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        yield cur
    finally:
        cur.close()
        conn.close()

    
def get_data(sql):
    with get_db_cursor() as cur:
        cur.execute(f"{sql} LIMIT 10;")
        data = cur.fetchall()
    return data


def get_discribe(table):
    with get_db_cursor() as cur:
        sql = f"SELECT * FROM information_schema.columns WHERE table_name = '{table}'"
        cur.execute(sql)
        data = cur.fetchall()
    return data
