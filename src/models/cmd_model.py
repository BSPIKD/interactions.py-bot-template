import os

import src.services.db_manager as dbs
import src.util.helper as h
import config as _conf


def get_cmd_type_by_name(cmd_name: str, db: int):
    with dbs.Connection(db) as conn:
        sql = f"select rights from config_cmds where name = ?"
        conn.cur.execute(sql, (cmd_name,))

