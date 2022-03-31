import os

import src.services.db_manager as dbs
import src.util.helper as h


def is_db_exist(db_name, is_server: bool = False):
    """
    Kontrola zda databáze existuje. V případě, že se jedná o server db nastaví se prefix
    :param db_name: Název databáze
    :param is_server: Jestli je databáze serverová
    :return:
    """
    db = db_name
    if is_server:
        db = f"{os.getenv('DB_PREFIX')}{db_name}"
    with dbs.Connection(select_db=False) as conn:
        sql = f"show databases like '{db}'"
        conn.cur.execute(sql)
        row = conn.cur.fetchone()
        return row is not None


def execute_sql_file(filename, database=os.getenv('DATABASE')):
    with dbs.Connection(database=database) as conn:
        for query in h.open_sql_file(filename):
            conn.cur.execute(query)


def create_database_if_not_exist(db_name):
    with dbs.Connection(select_db=False) as conn:
        if is_db_exist(db_name) is False:
            sql = f"create database if not exists `{db_name}`;"
            conn.cur.execute(sql)
            return True
        return False
