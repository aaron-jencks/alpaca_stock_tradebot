import sqlite3
import os.path as path

from settings import db_name, file_location
from tradebot.file_io import is_files_setup, setup_files
import tradebot.objects.stockdescriptor as sd
import tradebot.objects.limitdescriptor as ld
import tradebot.objects.balancedescriptor as bd


def execute_query(connection: sqlite3.Connection, query: str):
    print('Executing query:\n{}'.format(query))
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully:\n{}".format(query))
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection: sqlite3.Connection, query: str) -> list:
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")


def setup_table(name: str, columns: dict) -> str:
    """Creates a SQL Query for creating a table given the name and the column names/types"""
    result = "create table if not exists {} (".format(name)
    for k in columns.keys():
        result += k + " " + columns[k] + ", "
    return result[:-2] + ");"


def setup_record_insertion(table: str, tuple_names: str, records: list) -> str:
    result = "INSERT INTO\n\t{} {}\nVALUES\n".format(table, tuple_names)
    for r in records:
        result += "\t{},\n".format(r)
    return result[:-2] + ';'


def setup_record_update(table: str, properties: dict, selection_properties: dict) -> str:
    result = 'UPDATE\n\t{}\n\tSET'.format(table)
    for p in properties.keys():
        result += '\n\t{} = {},'.format(p,
                                        properties[p] if not isinstance(properties[p], str) else
                                        '"' + properties[p] + '"')
    result = result[:-1] + '\nWHERE'
    for s in selection_properties:
        result += '\n\t{} = {},'.format(s,
                                        selection_properties[s] if not isinstance(selection_properties[s], str) else
                                        '"' + selection_properties[s] + '"')
    return result[:-1]


def __setup_tables(conn: sqlite3.Connection):
    tables = sd.get_sql_tables()
    tables.append(ld.LimitDescriptor.create_sql_table())
    tables.append(bd.BalanceUpdate.create_sql_table())

    tbl_str = []
    for t in tables:
        tbl_str.append(setup_table(t['name'], t['properties']))

    for t in tbl_str:
        execute_query(conn, t)


def setup_db(directory: str) -> sqlite3.Connection:
    if not is_files_setup(directory):
        setup_files(directory)
    try:
        conn = sqlite3.connect(path.join(directory, db_name))
        __setup_tables(conn)
        return conn
    except sqlite3.Error as e:
        print('Something went wrong: {}'.format(e))
        return None


def connect_db(directory: str) -> sqlite3.Connection:
    if not is_files_setup(directory):
        return setup_db(directory)
    else:
        try:
            return sqlite3.connect(path.join(directory, db_name))
        except sqlite3.Error as e:
            print('Something went wrong: {}'.format(e))
            return None