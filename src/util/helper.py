import os
import io
from pathlib import Path

import config.conf as cf


def open_sql_file(filename):
    """
    Přečte sql soubor a vrátí jednotlivé dotazy v poli
    :param filename: Název souboru
    :return: Pole sql dotazů
    """
    with io.open(filename, mode='r', encoding='utf-8') as f:
        queries = f.read().split(';')
        del queries[-1]
        return queries


def get_dir_files(path, extension=None):
    files = []
    if extension is not None:
        for filename in os.listdir(path):
            if filename.endswith(extension):
                files.append(Path.joinpath(path, filename))
    else:
        for filename in os.listdir(path):
            files.append(Path.joinpath(path, filename))
    return files


def get_master_migration_files():
    return get_dir_files(cf.MASTER_MIGRATION, '.sql')


def get_server_migration_files():
    return get_dir_files(cf.SERVER_MIGRATION, '.sql')
