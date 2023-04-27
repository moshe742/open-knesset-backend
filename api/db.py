from contextlib import contextmanager

import psycopg2

from . import config
import re


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
    

# get list data
def get_data_list(start_query, limit, offset, order_by, qs):
    result = create_query_list(start_query, limit, offset, order_by, qs)
    if isinstance(result, Exception):
        return result
    query=result[0]
    values=result[1]
    try:
        with get_db_cursor() as cur:
            cur.execute(query,tuple(values))
            return cur.fetchall()
    except Exception as e:
        return e


# create query that returns data list
def create_query_list(start_query, limit: int = 0, offset: int = 0, order_by=None, qs: str | None = None):
    where_optional_args = []
    # options: limit, offset, order_by
    other_optional_args = []
    # values to put in placeholders in query
    values = []

    used_clause = ["limit", "offset", "order_by"]

    # add arguments to where clause
    if qs is not None:
        qs = qs.split('&')
        for item in qs:
            key, val = item.split('=')
            where_optional_args.append('"{0}" = %s'.format(key))
            values.append(val)
    # for key, val in request.args.items():
    #     if key not in used_clause:
    #         where_optional_args.append('"{0}" = %s'.format(key))
    #         values.append(val)

    # No arguments for where clause
    if not where_optional_args:
        where_optional_args.append("1 = 1")

    # add arguments to order by clause
    if order_by is not None:
        order_by_clause = ''
        pattern = r'^(\w+\s+(?i)(?:asc|desc))(?:,\s*\w+\s+(?i)(?:asc|desc))*\s*$'
        if not re.match(pattern, order_by):
            return ValueError('Must be this format: column1 asc/desc,column2 asc/desc..')

        for elemt in order_by.split(','):
            parts = elemt.split(' ')
            column = parts[0]
            order_type = parts[1]
            order_by_clause += f'"{column}" {order_type},'
        # remove last ','
        order_by_clause = order_by_clause[:-1]
        other_optional_args.append(f" ORDER BY {order_by_clause}")
    # add arguments to limit clause
    # if limit is not None:
    #     if not limit.isdigit() and not limit[1:].isdigit():
    #         return ValueError('Limit Must be an Integer!')
    if limit > 0:
        other_optional_args.append(" LIMIT %s")
        values.append(int(limit))
    # add arguments to offset clause
    # if offset is not None:
    #     if not offset.isdigit() and not offset[1:].isdigit():
    #         return ValueError('Offset Must be an Integer!')
    if offset > 0:
        other_optional_args.append(" OFFSET %s")
        values.append(int(offset))
    # create the query
    query = (
        f"{start_query} WHERE "
        + " AND ".join(where_optional_args)
        + "".join(other_optional_args)
    )
    return [query,values]


def get_discribe(table):
    with get_db_cursor() as cur:
        sql = f"SELECT * FROM information_schema.columns WHERE table_name = '{table}'"
        cur.execute(sql)
        data = cur.fetchall()
    return data
