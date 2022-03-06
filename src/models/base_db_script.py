import os

import src.services.db_manager as dbs
import src.util.helper as h


def is_db_exist(db_name):
    with dbs.Connection(select_db=False) as conn:
        sql = f"show databases like '{db_name}'"
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


def base_migration(migration_files, db=os.getenv('DATABASE'), is_new_run=False):
    with dbs.Connection(database=db) as conn:
        if is_new_run is True:
            for migration in migration_files:
                basename = os.path.basename(migration)
                execute_sql_file(filename=migration, database=db)
                conn.cur.execute('insert into _migrations (`name`) values (?)', (basename,))
                print(f'{db}>> Migrace {basename} byla úspěšně nasazena!')
        else:
            for migration in migration_files:
                basename = os.path.basename(migration)
                sql = f"select count(*) from _migrations where name = ?"
                conn.cur.execute(sql, (basename,))
                if conn.cur.fetchone()[0] < 1:
                    execute_sql_file(filename=migration, database=db)
                    conn.cur.execute('insert into _migrations (`name`) values (?)', (basename,))
                    print(f'{db}> Migrace {basename} byla úspěšně nasazena!')
                else:
                    print(f'<{db} Migrace {basename} již byla aplikována!')


def apply_master_migrations():
    is_new_run = create_database_if_not_exist(os.getenv('DATABASE'))
    base_migration(db=os.getenv('DATABASE'), is_new_run=is_new_run, migration_files=h.get_master_migration_files())


def apply_server_migrations(gid, name):
    is_guild_new = False
    guild_db_name = f"{os.getenv('DB_PREFIX')}{gid}"
    with dbs.Connection() as conn:
        sql = f"select count(*) from guilds where id = ?"
        conn.cur.execute(sql, (int(gid),))
        row = conn.cur.fetchone()
        if row[0] < 1:
            sql = f"insert into guilds (id, name, db_name) values (?, ?, ?)"
            conn.cur.execute(sql, (int(gid), name, guild_db_name))
            is_guild_new = create_database_if_not_exist(guild_db_name)
    base_migration(db=guild_db_name, is_new_run=is_guild_new, migration_files=h.get_server_migration_files())
