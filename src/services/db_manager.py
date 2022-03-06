import os

import mariadb


class Connection:
    def __init__(self, database=os.getenv("DATABASE"), select_db=True):
        if database is None:
            database = os.getenv("DATABASE")

        if select_db:
            self.conn = mariadb.connect(
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                host=os.getenv('HOST'),
                port=int(os.getenv('PORT')),
                database=database
            )
        else:
            self.conn = mariadb.connect(
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                host=os.getenv('HOST'),
                port=int(os.getenv('PORT'))
            )
        self.cur = self.conn.cursor()
        self.conn.autocommit = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()
