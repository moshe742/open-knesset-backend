from datetime import datetime,date
from functools import lru_cache
import json
import logging
from typing_extensions import Annotated
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor

import config

import re
from fastapi import Depends
from fastapi import responses

from fastapi import encoders
from typing import List, Dict

from decimal import Decimal

logger = logging.getLogger(__name__)
ITTER_SIZE=500


@lru_cache
def get_settings():
    return config.Settings()


def get_db_connection(
    settings: Annotated[config.Settings, Depends(get_settings)]
):
    return psycopg2.connect(
        host=settings.oknesset_db_host,
        port=settings.oknesset_db_port,
        database=settings.oknesset_db_name,
        user=settings.oknesset_db_user,
        password=settings.oknesset_db_password,
    )


@contextmanager
def get_db_cursor():
    conn = get_db_connection(get_settings())
    # Named cursor to be able stream data from database
    cur = conn.cursor(name='oknesset',cursor_factory=RealDictCursor)
    try:
        yield cur
    finally:
        cur.close()
        conn.close()


# get single data from table
def get_single_data(table, field, value):
    sql = f'select * from {table} where "{field}"={value}'
    with get_db_cursor() as cur:
        cur.execute(sql)
        data = cur.fetchone()
        if data is None:
            return TypeError('No such data exists!')
    return data


# get all known info about current minister or knesset member
def get_fully_today_member(query, value=None):
    try:
        with get_db_cursor() as cur:
            cur.execute(query, value)
            data = cur.fetchone()
            if data is None:
                raise ValueError('No such member exist!')
    except Exception as e:
        return e
    return data

# Get info about knesset members
# is_current = true --> current Knesset members
# is_current = false --> inactive Knesset members
# knesset_num --> Knesset period of the Knesset member
def get_members(query,is_current:bool,knesset_num:int):
    try:
        with get_db_cursor() as cur:
            if is_current:
                if(knesset_num==None):
                    cur.execute('select max("KnessetNum") from knesset_kns_knessetdates')
                    knesset_number = cur.fetchone()
                    is_current_params=(knesset_number['max'],
                                 knesset_number['max'],
                                 knesset_number['max'],
                                 knesset_number['max'],
                                 is_current)
                    cur.execute(query,is_current_params)
                    data = cur.fetchall()
                else:
                    is_current_params=(knesset_num,
                                 knesset_num,
                                 knesset_num,
                                 knesset_num,
                                 is_current)
                    cur.execute(query,is_current_params)
                    data = cur.fetchall()
               
            else:
                is_current_params=(knesset_num,
                                 knesset_num,
                                 knesset_num,
                                 knesset_num,
                                 is_current)
                cur.execute(query,is_current_params)
                data = cur.fetchall()
    except Exception as e:
        return e
    return data

# Get info about some Knesset member
def get_members_info(query,mk_individual_id:int): 
    try:
        with get_db_cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            # Two options:
            # 1. No such 'mk_individual_id' in database
            # 2. 'mk_individual_id' exist but no data for him
            if (not(is_mk_individual_exist(mk_individual_id)) 
                or len(data) == 0 ):
                return TypeError('No such data exists!')
    except Exception as e:
        return e
    return data

def is_mk_individual_exist(mk_individual_id: int):
    try:
        with get_db_cursor() as cur:
            cur.execute("""SELECT mk_individual_id
                            FROM members_mk_individual 
                            WHERE mk_individual_id=%s""",
                            (mk_individual_id,))
            is_member_exist=cur.fetchone()
            if is_member_exist==None:
                return False
            return True
    except Exception as e:
        return e
        


# Retrieve a list of data results.
# Always streaming result from database in batches of ITTER_SIZE.
# Streaming result from database is available with named cursor 
# When using 'psycopg2' library
# The declaration of the named cursor is handled within 
# the get_db_cursor() function.
# For example, name = 'oknesset'.
def get_data_list(start_query, limit, offset, order_by, qs):
    if limit > 10000:
        return ValueError("Can't use limit value above 10000")
    elif limit < 1:
        return ValueError("Can't use limit value under 1")
    result = create_query_list(start_query, limit, offset, order_by, qs)
    if isinstance(result, Exception):
        return result
    query = result[0]
    values = result[1]
    try:
        # For small data size sending normal JSONResponse 
        # without streaming the result to the client
        if(limit<=ITTER_SIZE):
            with get_db_cursor() as cur:
                cur.execute(query, tuple(values))
                data = cur.fetchall()
                data = json_serialize(data)
                return responses.JSONResponse(content=data)  
        # For large data size sending stream response
        # StreamingResponse to the client   
        else:        
            return responses.StreamingResponse(
                    streaming_response_iterator(query,values),
                    media_type="application/json"
                )
    except Exception as e:
        return e

# Making the generator for streaming the result to the client
def streaming_response_iterator(query,values):
        try:
            yield b"["
            with get_db_cursor() as cur:
                cur.itersize = ITTER_SIZE
                cur.execute(query, tuple(values))
                for i, obj in enumerate(cur):
                    item = encoders.jsonable_encoder(obj)
                    if i > 0:
                        yield b","
                    yield json.dumps(item).encode()
                yield b"]"
        except Exception as e:
            return e


def json_serialize(data: List[Dict]):
    def serialize_value(value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(value, date):
            return value.strftime("%d/%m/%y")
        elif isinstance(value, Decimal):
            return float(value)
        else:
            return value

    return [
        {
            key: serialize_value(value) for key, value in row.items()
        }
        for row in data
    ]


# create query that returns data list
def create_query_list(
    start_query, limit: int = 0, offset: int = 0,
    order_by=None, qs: str | None = None
):
    # options: limit, offset, order_by
    where_optional_args = []
    # options: limit, offset, order_by
    other_optional_args = []
    # values to put in placeholders in query
    values = []
    crc32c = False
    # add arguments to where clause
    if qs:
        qs = qs.split('&')
        for item in qs:
            # dealing with crc32c format
            if item[-2:] == '==':
                item = item[:-2]
                crc32c = True
            key, val = item.split('=')
            # checking if it's crc32c format
            if crc32c:
                val += '=='
                crc32c = False
            # checks if it's simple array of strings or integers
            if '[' in val:
                val_splited = val[1:-1].split(',')
                # checks if it's integers array
                try:
                    val = [int(element) for element in val_splited]
                    val = str(val)
                # if here, it's strings array
                except Exception:
                    val = str(val).replace("'", '"')

                val = val.replace('\\\\', '\\')
                values.append(val)
                where_optional_args.append('"{0}" @> %s'.format(key))
            # checks if it's array of objects
            elif '<' in val:
                key_splited = key.split('_')
                object_key = key_splited[0]
                # checks if field of object has two words combine
                if len(key_splited) == 3:
                    object_field = '{0}_{1}'.format(
                        key_splited[1],
                        key_splited[2]
                    )
                # if here, field of object is one word
                else:
                    object_field = key_splited[1]

                # checks if field of object is integer
                if not (val[1:-1].isdigit()):
                    val = '[{{"{0}": "{1}"}}]'.format(object_field, val[1:-1])
                # if here, field of object is string
                else:
                    val = '[{{"{0}": {1}}}]'.format(object_field, val[1:-1])
                values.append(val)
                where_optional_args.append(
                   '"{0}" @> %s'.format(object_key)
                )
            # if here, it's simple data type integer, string or bool
            else:
                where_optional_args.append('"{0}" = %s'.format(key))
                values.append(val)

    # No arguments for where clause
    if not where_optional_args:
        where_optional_args.append("1 = 1")

    # add arguments to order by clause
    if order_by is not None:
        order_by_clause = ''
        pattern = r'^(\w+\s+(?:asc|desc))(?:,\s*\w+\s+(?:asc|desc))*\s*$'
        if not re.match(pattern, order_by, re.IGNORECASE):
            return ValueError('Must be this format:'
                              'column1 asc/desc,column2 asc/desc..')

        for elemt in order_by.split(','):
            parts = elemt.split(' ')
            column = parts[0]
            order_type = parts[1]
            order_by_clause += f'"{column}" {order_type},'
        # remove last ','
        order_by_clause = order_by_clause[:-1]
        other_optional_args.append(f" ORDER BY {order_by_clause}")
    # add arguments to limit clause
    if limit > 0:
        other_optional_args.append(" LIMIT %s")
        values.append(int(limit))
    # add arguments to offset clause
    if offset > 0:
        other_optional_args.append(" OFFSET %s")
        values.append(int(offset))
    # create the query
    query = (
        f"{start_query} WHERE "
        + " AND ".join(where_optional_args)
        + "".join(other_optional_args)
    )
    return [query, values]
