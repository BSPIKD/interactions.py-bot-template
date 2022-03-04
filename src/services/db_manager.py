import os

import mariadb


class Connection:
    def __init__(self, database=os.getenv("DATABASE")):
        if database is None:
            database = os.getenv("DATABASE")

        self.conn = mariadb.connect(
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'),
            port=int(os.getenv('PORT')),
            database=database
        )
        self.cur = self.conn.cursor()
        self.conn.autocommit = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()
