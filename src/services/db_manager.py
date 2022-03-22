import os

import mariadb


class Connection:
    def __init__(self, database=os.getenv("DATABASE"), select_db=True):
        db = database
        if db is None:
            db = os.getenv("DATABASE")
        elif db != os.getenv("DATABASE"):
            db = f"{os.getenv('DB_PREFIX')}{db}"

        if select_db:
            self.conn = mariadb.connect(

                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                host=os.getenv('HOST'),
                port=int(os.getenv('PORT')),
                database=db
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
