import sqlite3
import os.path as path

from settings import db_name, file_location
from tradebot.file_io import is_files_setup, setup_files
import tradebot.objects.stockdescriptor as sd
import tradebot.objects.limitdescriptor as ld
import tradebot.objects.balancedescriptor as bd


def execute_query(connection: sqlite3.Connection, query: str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")


def setup_table(name: str, columns: dict) -> str:
    """Creates a SQL Query for creating a table given the name and the column names/types"""
    result = "CREATE TABLE IF NOT EXISTS {} (".format(name)
    for k in columns.keys():
        result += k + " " + columns[k] + ", "
    return result[:-2] + ");"


def __setup_tables(conn: sqlite3.Connection):
    tables = sd.get_sql_tables()
    tables.append(ld.LimitDescriptor.create_sql_table())
    tables.append(bd.BalanceUpdate.create_sql_table())

    tbl_str = []
    for t in tables:
        tbl_str.append(setup_table(t['name'], t['properties']))

    for t in tbl_str:
        execute_query(conn, t)


def setup_db() -> sqlite3.Connection:
    if not is_files_setup():
        setup_files()
    try:
        conn = sqlite3.connect(path.join(file_location, db_name))
        __setup_tables(conn)
        return conn
    except sqlite3.Error as e:
        print('Something went wrong: {}'.format(e))
        return None