import os

from src.services.db_manager import Connection
import src.util.helper as _h


class BaseDb:
    def __init__(self, database: int):
        if database == 0:
            self.db = os.getenv("DATABASE")
        else:
            self.db = database
        # Todo: IDEA - udělat connection jednou a pak close method

    def is_db_exist(self, is_server: bool = False) -> bool:
        db = self.db
        if is_server:
            db = f"{os.getenv('DB_PREFIX')}{db}"
        with Connection(select_db=False) as conn:
            sql = f"show databases like '{db}'"
            conn.cur.execute(sql)
            return conn.cur.fetchone() is not None

    def execute_sql_file(self, filename):
        with Connection(self.db) as conn:
            for query in _h.open_sql_file(filename):
                conn.cur.execute(query)


    def create_database_if_not_exist(self, is_server: bool = False):
        db = self.db
        if is_server is True:
            db = f"{os.getenv('DB_PREFIX')}{self.db}"

        with Connection(select_db=False) as conn:
            if self.is_db_exist() is False:
                # Databáze neexistuje, je potřeba jí vytvořit
                sql = f"create database if not exists `{db}`;"
                conn.cur.execute(sql)
                self.__create_migration_table()
                return True
            return False


    def __create_migration_table(self):
        with Connection(self.db) as conn:
            sql = f"""create table _migrations(
                        name        varchar(255) not null,
                        `timestamp` timestamp default current_timestamp());"""
            conn.cur.execute(sql)
            return True


    def get_config(self, key: str):
        with Connection(self.db) as conn:
            sql = f"select value from config where `key` = ?"
            conn.cur.execute(sql, (key,))
            return conn.cur.fetchone()[0]


    def update_config(self, key: str, value: str):
        with Connection(self.db) as conn:
            sql = f"update config set value = ? where `key` = ?"
            conn.cur.execute(sql, (value, key))
            return True

    def get_cmd_rights(self, cmd_name: str):
        """
        Get commands user rights by command name
        :param cmd_name:
        :return:
        """
        with Connection(self.db) as conn:
            sql = f"select rights from config_cmds where name = ?"
            conn.cur.execute(sql, (cmd_name,))
            return conn.cur.fetchone()[0]

    def get_cmd_by_name(self, cmd_name: str):
        """
        Check if command exist in database
        :param cmd_name:
        """
        with Connection(self.db) as conn:
            sql = f"select * from config_cmds where name = ?"
            conn.cur.execute(sql, (cmd_name,))
            data = conn.cur.fetchone()
            if data is None:
                return False, False  # Neexistuje
            else:
                if int(data[3]) == 1:
                    return True, True  # Existuje a je zapnutý
                return True, False  # Existuje a je vypnutý

    def get_count_of_unset_configs(self):
        with Connection(self.db) as conn:
            sql = f"select * from config where is_important = 1 and value is null"
            conn.cur.execute(sql)
            rows = conn.cur.fetchall()
            if len(rows) > 0:
                return False, rows
            return True, None

    def log_db(self, cls: str, method: str, line: int, tp: str, message: str):
        with Connection(self.db) as conn:
            sql = f"insert into `logs` (class, method, line, type, message) " \
                  f"values (?, ?, ?, ?, ?)"
            conn.cur.execute(sql, (cls, method, line, tp, method))
