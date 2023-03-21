import os
import psycopg2


def get_db_connection():
    return psycopg2.connect(
        host=os.environ['HOST'],
        port=os.environ['PORT'],
        database=os.environ['DATABASE'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
    )
    
    
def get_data(sql):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"{sql} LIMIT 10;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data
    
def get_discribe(table):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = f"SELECT * FROM information_schema.columns WHERE table_name = '{table}'"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data
    
    
