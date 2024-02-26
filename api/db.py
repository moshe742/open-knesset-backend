from datetime import datetime, date
from functools import lru_cache
import itertools
import json
import logging
from typing_extensions import Annotated
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor

import config

from fastapi import Depends
from fastapi import responses

from fastapi import encoders
from typing import List, Dict
from fastapi import responses

from fastapi import encoders
from typing import List, Dict

from decimal import Decimal
from decimal import Decimal

logger = logging.getLogger(__name__)
ITTER_SIZE = 500


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
def get_db_cursor(cursor_name: str = 'oknesset'):
    conn = get_db_connection(get_settings())
    """
    Context manager for acquiring and using a database cursor.

    This function returns a context manager that can be used with the `with` statement
    to acquire a database cursor, execute operations, and automatically close the cursor
    and connection when the block is exited.

    Usage:
    ```
    with get_db_cursor() as cursor:
        # Perform database operations using the cursor
        cursor.execute("SELECT * FROM your_table")
        result = cursor.fetchall()
        # Do something with the result

    # Cursor and connection are automatically closed outside the 'with' block
    ```

    Returns:
    psycopg2.extensions.cursor: A database cursor with a RealDictCursor factory.

    Raises:
    Exception: Any exception that may occur during the acquisition of the cursor or
               execution of operations within the 'with' block.
    """
    if cursor_name:
        cur = conn.cursor(name=cursor_name, cursor_factory=RealDictCursor)
    else:
        cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cur
    finally:
        cur.close()
        conn.close()


def get_single_data(table: str, field: str, value: int):
    """
    Retrieve a single record from the specified database table based on the provided criteria.

    This function executes a SELECT query on the specified table, using the provided field and value
    to filter the results. It returns the first matching record or raises an exception if no match is found.

    Usage:
    ```
    try:
        result = get_single_data("your_table", "your_field", "desired_value")
        # Do something with the result
    except TypeError as e:
        print(f"Error: {e}")
    ```

    Args:
    - table (str): The name of the database table to query.
    - field (str): The field in the table to use as a filter.
    - value (int): The value to match in the specified field.

    Returns:
    dict: A dictionary representing the first matching record in the specified table.

    Raises:
    TypeError: If no data is found matching the specified criteria.

    """
    sql = f'select * from {table} where "{field}"={value}'
    try:
        with get_db_cursor() as cur:
            cur.execute(sql)
            data = cur.fetchone()
            if data is None:
                return TypeError(
                    'No such data exists! Please enter another ID')
    except Exception as e:
        logger.critical("critical error", e)
    return data


def get_fully_today_member(query: str, value: int):
    """
    Retrieve all known information about the current minister or Knesset member based on the provided query.

    This function executes a custom query on the database to retrieve information about the current minister or
    Knesset member. The query and optional value are used to filter the results. It returns a dictionary with the
    known information about the member or raises an exception if no match is found.

    Usage:
    ```
    try:
        result = get_fully_today_member("SELECT * FROM your_table WHERE condition = %s", ("desired_value",))
        # Do something with the result
    except ValueError as e:
        print(f"Error: {e}")
    ```

    Args:
    - query (str): The SQL query to execute for retrieving member information.
    - value (int): The value to be used in the query as a parameter.

    Returns:
    dict: A dictionary containing all known information about the current minister or Knesset member.

    Raises:
    TypeError: If no member is found based on the provided query and value.

    """
    try:
        with get_db_cursor() as cur:
            cur.execute(query, value)
            data = cur.fetchone()
            if data is None:
                return TypeError(
                    'No such member exist! Please enter another ID')
    except Exception as e:
        logger.critical("critical error", e)
    return data


def get_members(query, is_current: bool, knesset_term: int = None):
    """
    Retrieve information about members based on the provided query, current status, and Knesset number.

    This function executes a custom query on the database to retrieve information about members based on the
    specified criteria. The 'query' parameter defines the SQL query to execute, 'is_current' is a boolean
    indicating whether to retrieve current or past members, and 'knesset_num' is an optional parameter
    specifying the Knesset number for filtering.

    Usage:
    ```
    try:
        result = get_members("SELECT * FROM your_table WHERE condition = %s", is_current=True, knesset_num=24)
        # Do something with the result
    except Exception as e:
        print(f"Error: {e}")
    ```

    Args:
    - query (str): The SQL query to execute for retrieving member information.
    - is_current (bool): A boolean indicating whether to retrieve information about current members.
    - knesset_num (int, optional): The Knesset number for filtering members. If not provided, the function
      retrieves information for the latest Knesset.

    Returns:
    list: A list of dictionaries containing information about members based on the query and criteria.

    Raises:
    Exception: Any exception that may occur during the execution of the query.

    """
    try:
        with get_db_cursor('max') as cur_max, get_db_cursor('data') as cur_data:
            if is_current:
                if (knesset_term is None):
                    cur_max.execute(
                        'select max("KnessetNum") from knesset_kns_knessetdates')
                    knesset_term = cur_max.fetchone()['max']
                    cur_data.execute(
                        query, {
                            'is_current': is_current, 'knesset_term': knesset_term})
                    data = cur_data.fetchall()
                else:
                    cur_data.execute(
                        query, {
                            'is_current': is_current, 'knesset_term': knesset_term})
                    data = cur_data.fetchall()

            else:
                cur_data.execute(
                    query, {
                        'is_current': is_current, 'knesset_term': knesset_term})
                data = cur_data.fetchall()
    except Exception as e:
        logger.critical("critical error", e)
    return data


def get_member(query, mk_individual_id: int, knesset_term: int = None):
    """
    Retrieve information about a member of the Knesset (Israeli Parliament) based on the provided query.

    Parameters:
    - query (str): SQL query to fetch data from the database.
    - mk_individual_id (int): The unique identifier for the member of Knesset.
    - knesset_term (int, optional): The Knesset term for which the information is requested.
      If not provided, the function will automatically use the latest available term.

    Returns:
    dict: A dictionary containing information about the member of Knesset, or None if no data is found.

    Note:
    If an error occurs during the execution, a critical error message is logged, and the function returns None.

    Example:
    ```
    result = get_member(query, mk_individual_id=123, knesset_term=24)
    ```

    """
    try:
        # Using two different cursors not not get error with execute more than
        # once
        with get_db_cursor('max') as cur_max, get_db_cursor('data') as cur_data:
            if (knesset_term is None):
                cur_max.execute(
                    'select max("KnessetNum") as max_term from knesset_kns_knessetdates')
                knesset_term = cur_max.fetchone()['max_term']
            cur_data.execute(query,
                             {'mk_individual_id': mk_individual_id,
                              'knesset_term': knesset_term})
            data = cur_data.fetchone()
            if not (is_mk_individual_exist(mk_individual_id)):
                return TypeError(
                    'No such data exists! Please enter another ID')
            elif not (is_knesset_term_exist(knesset_term)):
                return TypeError(
                    'No such data exists! Please enter another Knesset term')
    except Exception as e:
        logger.critical("critical error", e)
    return data


def get_member_by_committee(committee: int | str):
    """
    Retrieve distinct member IDs associated with a specified committee.

    Parameters:
    - committee (int | str): Either the committee ID (if int) or a string representing part or all of the committee name.

    Returns:
    - list: A list of distinct member IDs associated with the specified committee.

    Examples:
    ```
    # Example 1: Retrieve individual IDs for members of committee with ID 101
    members_ids = get_member_by_committee(101)

    # Example 2: Retrieve individual IDs for members of committee with name 'Finance Committee'
    members_ids = get_member_by_committee('Finance Committee')
    ```
    """
    try:
        with get_db_cursor('data') as cur_data:
            if isinstance(committee, int):
                cur_data.execute(
                    "select DISTINCT(mk_individual_id) from members_mk_individual_committees where committee_id = %s",
                    (committee,
                     ))
            else:
                cur_data.execute(
                    "select DISTINCT(mk_individual_id) from members_mk_individual_committees where committee_name like '%{committee}%'",
                    (committee,
                     ))
            data = cur_data.fetchall()
    except Exception as e:
        logger.critical("critical error", e)
    return data


def get_member_by_faction(faction: int | str):
    """
    Retrieve distinct member IDs associated with a specified faction.

    Parameters:
    - faction (int | str): Either the faction ID (if int) or a string representing part or all of the faction name.

    Returns:
    - list: A list of distinct member IDs associated with the specified faction.

    Examples:
    ```
    # Example 1: Retrieve individual IDs for members of faction with ID 42
    members_ids_1 = get_member_by_faction(42)

    # Example 2: Retrieve individual IDs for members of faction with name 'Finance'
    members_ids_2 = get_member_by_faction('Finance')
    ```
    """
    try:
        with get_db_cursor('data') as cur_data:
            if isinstance(faction, int):
                cur_data.execute(
                    "select DISTINCT(mk_individual_id) from members_mk_individual_factions where faction_id = %(faction_id)s", {
                        "faction_id": faction})
            else:
                cur_data.execute(
                    "select DISTINCT(mk_individual_id) from members_mk_individual_factions where faction_name like %(faction_name)s", {
                        "faction_name": '%' + faction + '%'})
            data = cur_data.fetchall()
    except Exception as e:
        logger.critical("critical error", e)
    return data


def get_member_by_faction_chairperson(faction: int | str):
    """
    Retrieves a list of distinct individual IDs associated with members who have served as chairpersons
    of the specified faction.

    Parameters:
    - faction (int | str): The identifier (ID) or name of the faction to retrieve members for.
                          If an integer is provided, it is treated as the faction ID; if a string is provided,
                          it is treated as a case-insensitive search for the faction name.

    Returns:
    - list: A list of distinct individual IDs associated with members who served as chairpersons of the specified faction.

    Example:
    ```
    # Retrieve individual IDs for members of faction with ID 42
    members_ids = get_member_by_faction_chairperson(42)

    # Retrieve individual IDs for members of faction with name 'Finance'
    members_ids = get_member_by_faction_chairperson('Finance')
    ```
    """
    try:
        with get_db_cursor() as cur_data:
            if isinstance(faction, int):
                cur_data.execute(
                    "select DISTINCT(mk_individual_id) from members_mk_individual_faction_chairpersons where faction_id = %(faction_id)s", {
                        "faction_id": faction})
            else:
                cur_data.execute(
                    "select DISTINCT(mk_individual_id) from members_mk_individual_faction_chairpersons where faction_name like %(faction_name)s", {
                        "faction_name": '%' + faction + '%'})
            data = cur_data.fetchall()
    except Exception as e:
        logger.critical("critical error", e)
    return data


def get_member_by_govministries(govministry: int | str):
    """
    Retrieve distinct member IDs associated with a specified government ministry.

    Parameters:
    - govministry (int | str): Either the government ministry ID (if int) or a string representing part or all of the government ministry name.

    Returns:
    - list: A list of distinct member IDs associated with the specified government ministry.

    Examples:
    ```
    # Example 1: Retrieve individual IDs for members of government ministry with ID 101
    members_ids_1 = get_member_by_govministries(101)

    # Example 2: Retrieve individual IDs for members of government ministry with name 'Health Ministry'
    members_ids_2 = get_member_by_govministries('Health Ministry')
    """
    try:
        with get_db_cursor() as cur_data:
            if isinstance(govministry, int):
                cur_data.execute(
                    "select DISTINCT(mk_individual_id) from members_mk_individual_govministries where govministry_id = %(govministry_id)s", {
                        "govministry_id": govministry})
            else:
                cur_data.execute(
                    "select DISTINCT(mk_individual_id) from members_mk_individual_govministries where govministry_name like %(govministry_name)s", {
                        "govministry_name": '%' + govministry + '%'})
            data = cur_data.fetchall()
    except Exception as e:
        logger.critical("critical error", e)
    return data


def get_member_by_name(name: str):
    """
    Retrieve distinct member IDs associated with a specified name.

    Parameters:
    - name (str): The name or parts of the name to search for.

    Returns:
    - list: A list of distinct member IDs associated with the specified name.

    Examples:
    ```
    # Example 1: Retrieve individual IDs for members with the name 'John Doe'
    members_ids_1 = get_member_by_name('John Doe')

    # Example 2: Retrieve individual IDs for members with the name 'Jane'
    members_ids_2 = get_member_by_name('Jane')

    # Example 3: Retrieve individual IDs for members with the name 'Alice Smith Junior'
    members_ids_3 = get_member_by_name('Alice Smith Junior')
    ```
    Note:
    - The function searches for members based on permutations of the provided name parts.
    - It queries the database table 'members_mk_individual' and also considers alternative names stored in the 'altnames' field.
    - The results are distinct member IDs associated with the specified name or name parts.
    - If no matching member is found, a ValueError is raised.
    - If the provided name has too many parts (more than four), a ValueError is raised.
    """
    try:
        with get_db_cursor(None) as cur:
            results = []
            name_parts = name.split()
            if len(name_parts) > 4:
                return ValueError(
                    'too many name parts! Please enter at most four name parts')
            name_permutations = [
                ' '.join(p) for p in itertools.permutations(name_parts)]
            for name_permutation in name_permutations:
                cur.execute(
                    "select mk_individual_id from members_mk_individual where mk_individual_first_name || ' ' || mk_individual_name like %(name)s", {
                        "name": '%' + name_permutation + '%'})
                data = cur.fetchall()
                results.extend(data)
                cur.execute(
                    "select mk_individual_id from (select mk_individual_id, jsonb_array_elements_text(altnames) altname from members_mk_individual) a where altname like %(name)s", {
                        "name": '%' + name_permutation + '%'})
                data = cur.fetchall()
                results.extend(data)
            if len(results) == 0:
                return ValueError(
                    'There is no member with this name! Please enter another name or consider another spelling')
    except Exception as e:
        logger.critical("critical error", e)
    # Using 'set' to get distinct results and convert back to list
    results = list({tuple(d.items()) for d in results})
    return results


def is_mk_individual_exist(mk_individual_id: int):
    """
    Check if a member with the specified mk individual ID exists in the database.

    This function executes a query to check if a member with the provided mk individual ID exists in the
    'members_mk_individual' table of the database. It returns a boolean indicating whether the member exists.

    Usage:
    ```
    if is_mk_individual_exist(123):
        print("Member exists!")
    else:
        print("Member does not exist!")
    ```

    Args:
    - mk_individual_id (int): The unique individual ID of the member.

    Returns:
    bool: True if the member with the specified MK individual ID exists, False otherwise.

    """
    try:
        with get_db_cursor() as cur:
            cur.execute("""SELECT mk_individual_id
                            FROM members_mk_individual
                            WHERE mk_individual_id=%s""",
                        (mk_individual_id,))
            is_member_exist = cur.fetchone()
            if is_member_exist is None:
                return False
            return True
    except Exception as e:
        logger.critical("critical error", e)


def is_knesset_term_exist(knesset_term: int):
    """
    Check if the specified Knesset term exists in the database.

    This function executes a query to check if a Knesset term exists in the
    'knesset_kns_knessetdates' table of the database. It returns a boolean indicating whether the Knesset term exists.

    Usage:
    ```
    if is_knesset_exist(24):
        print("Knesset term exists!")
    else:
        print("Knesset term does not exist!")
    ```

    Args:
    - knesset_term (int): Knesset term.

    Returns:
    bool: True if the Knesset term exists, False otherwise.

    """
    try:
        with get_db_cursor() as cur:
            cur.execute("""SELECT "KnessetNum"
                            FROM knesset_kns_knessetdates
                            WHERE "KnessetNum"=%s""",
                        (knesset_term,))
            is_term_exist = cur.fetchone()
            if is_term_exist is None:
                return False
            return True
    except Exception as e:
        logger.critical("critical error", e)


def get_data_list(
        start_query: str,
        limit: int,
        offset: int,
        order_by: str,
        qs: str):
    """
    Retrieve a list of data from the database based on the provided parameters.

    This function creates a query using the provided parameters (limit, offset, order_by, qs), executes the query
    on the database, and returns the results. Depending on the size of the data, it either sends a normal
    JSONResponse for small data or uses StreamingResponse for large data to enhance performance.

    Usage:
    ```
    try:
        result = get_data_list(
            "SELECT * FROM your_table WHERE condition = %s",
            limit=100,
            offset=0,
            order_by="column1 asc,column2 desc",
            qs="param1=value1&param2=value2"
        )
        # Handle the result accordingly
    except ValueError as e:
        print(f"ValueError: {e}")
    ```

    Args:
    - start_query (str): The initial part of the SQL query.
    - limit (int): The maximum number of rows to return.
    - offset (int): The number of rows to skip before starting to return data.
    - order_by (str): A comma-separated string specifying the columns and their sort order (e.g., 'column1 asc,column2 desc').
    - qs (str): A string constructed from key-value pairs joined by '&'. For example, 'param1=value1&param2=value2'.

    Returns:
    Union[responses.JSONResponse, StreamingResponse]: A JSONResponse or StreamingResponse
    based on the size of the data.

    Raises:
        ValueError:
            - If the limit is above 10000 or below 1.
            - If the 'order by' parameter is of the wrong format.
    """
    if limit > 10000:
        return ValueError("Can't use limit value above 10000")
    elif limit < 1:
        return ValueError("Can't use limit value under 1")
    result = create_query_list(start_query, limit, offset, order_by, qs)
    if isinstance(result, ValueError):
        return result
    query = result[0]
    values = result[1]
    try:
        # For small data size sending normal JSONResponse
        # without streaming the result to the client
        if (limit <= ITTER_SIZE):
            with get_db_cursor() as cur:
                cur.execute(query, tuple(values))
                data = cur.fetchall()
                data = json_serialize(data)
                return responses.JSONResponse(content=data)
        # For large data size sending stream response
        # StreamingResponse to the client
        else:
            return responses.StreamingResponse(
                streaming_response_iterator(query, values),
                media_type="application/json"
            )
    except Exception as e:
        logger.critical("critical error", e)


def streaming_response_iterator(query: str, values):
    """
    Stream data from the database as a JSON array in a FastAPI response.

    This function executes a query on the database and streams the results as a JSON array. It uses FastAPI's
    `jsonable_encoder` to convert objects to JSON-serializable format. The data is yielded in chunks to enhance
    streaming behavior.

    Usage:
    ```
    # Assuming 'query' and 'values' are properly defined
    response_iterator = streaming_response_iterator(query, values)
    return StreamingResponse(response_iterator, media_type="application/json")
    ```

    Args:
    - query (str): The SQL query to execute for streaming data.
    - values (Any): The values to be used in the query as parameters.

    Yields:
    bytes: Chunks of bytes representing a JSON array.

    """
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
        logger.critical("critical error 500", e)


def json_serialize(data: List[Dict]):
    """
    Serialize a list of dictionaries to JSON-compatible format.

    This function takes a list of dictionaries and serializes it to a format suitable for JSON serialization.
    It converts datetime objects to strings in the format "%Y-%m-%dT%H:%M:%S", date objects to strings in
    the format "%d/%m/%y", and Decimal objects to floats. Other types remain unchanged.

    Usage:
    ```
    data = [{'key1': value1, 'key2': value2}, {'key1': value3, 'key2': value4}]
    serialized_data = json_serialize(data)
    # Use serialized_data in JSON-related operations
    ```

    Args:
    - data (List[Dict]): A list of dictionaries to be serialized.

    Returns:
    List[Dict]: A new list of dictionaries with values serialized for JSON compatibility.

    """
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


def create_query_list(
    start_query: str, limit: int, offset: int,
    order_by=None, qs: str | None = None
):
    """
    Create a parameterized SQL query and a list of values based on the provided parameters.

    This function constructs a parameterized SQL query and a list of values for executing the query. It processes
    optional parameters such as limit, offset, order_by, and query string (qs) to create a dynamic WHERE clause.

    Usage:
    ```
    result = create_query_list(
        "SELECT * FROM your_table",
        limit=100,
        offset=0,
        order_by="column1 asc,column2 desc",
        qs="param1=value1&param2=value2"
    )
    # Use the result in executing the query
    ```

    Args:
    - start_query (str): The initial part of the SQL query.
    - limit (int, optional): The maximum number of rows to return. Default is 100.
    - offset (int, optional): The number of rows to skip before starting to return data. Default is 0.
    - order_by (str, optional): A string specifying the columns and their sort order (e.g., 'column1 asc,column2 desc').
      Default is None.
    - qs (str, optional): A string constructed from key-value pairs joined by '&'. For example, 'param1=value1&param2=value2'.
      Default is None.

    Returns:
    Union[List, ValueError]: A list containing the constructed query and values, or a ValueError if the order_by
    parameter does not match the required format.

    Raises:
    ValueError: If the order_by parameter does not match the required format.

    """
    # options: model fields
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
        other_optional_args.append(f" ORDER BY {order_by}")
    # add arguments to limit clause
    if limit > 0:
        other_optional_args.append(" LIMIT %s")
        values.append(int(limit))
    # add arguments to offset clause
    if offset > 0:
        other_optional_args.append(" OFFSET %s")
        values.append(int(offset))
    # create the query
    if (qs):
        query = (
            f"{start_query} WHERE "
            + " AND ".join(where_optional_args)
            + "".join(other_optional_args)
        )
    else:
        query = (
            f"{start_query}" + "".join(other_optional_args)
        )
    return [query, values]
