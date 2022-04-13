import os
import logging

from pyfiglet import figlet_format

import src.services.db_manager as dbs
import src.util.helper as h
import src.models.base_db_script as _base

from termcolor import colored, cprint



def base_migration(migration_files, db=os.getenv('DATABASE'), is_server: bool = False):
    # Kontrola a vytvoření databáze jestli neexistuje
    is_db_new = _base.create_database_if_not_exist(db, is_server)

    with dbs.Connection(database=db) as conn:
        if is_db_new is True:
            # Byla vytvořena nová db, je potřeba nahrát všechny migrace
            for migration in migration_files:
                basename = os.path.basename(migration)
                # executnem všechny dotazy v migraci
                _base.execute_sql_file(filename=migration, database=db)
                conn.cur.execute('insert into _migrations (`name`) values (?)', (basename,))
                cprint(f'{db}>> Migrace {basename} byla úspěšně nasazena!', 'green', attrs=['bold'])
        else:
            # Databáze existuje a je potřeba nahrát nové migrace
            for migration in migration_files:
                basename = os.path.basename(migration)
                sql = f"select count(*) from _migrations where name = ?"
                conn.cur.execute(sql, (basename,))
                if conn.cur.fetchone()[0] < 1:
                    _base.execute_sql_file(filename=migration, database=db)
                    conn.cur.execute('insert into _migrations (`name`) values (?)', (basename,))
                    cprint(f'{db}> Migrace {basename} byla úspěšně nasazena!', 'green', attrs=['bold'])
                else:
                    cprint(f'<{db} Migrace {basename} již byla aplikována!', 'yellow')


def apply_master_migrations():
    base_migration(migration_files=h.get_master_migration_files(), db=os.getenv('DATABASE'))


def apply_server_migrations(gid, name):
    is_guild_new = False
    guild_db_name = f"{os.getenv('DB_PREFIX')}{gid}"

    base_migration(migration_files=h.get_server_migration_files(), db=gid, is_server=True)

    cprint(figlet_format('Setup complete', font='standard'), 'blue')
