import os
import io
from pathlib import Path
from termcolor import cprint
from pyfiglet import figlet_format

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


def parse_cmd_name(cmd: str):
    return cmd.replace(' ', '-')


def print_info():
    cprint(figlet_format('Author', font='larry3d'), 'cyan')
    cprint(figlet_format('Dom-kun#5353', font='standard'), 'red')
    cprint(figlet_format('Bot', font='larry3d'), 'cyan')
    cprint(figlet_format('Template v0.1', font='standard'), 'red')
    cprint(figlet_format('--------', font='larry3d'), 'blue')
    cprint(figlet_format('BOT IS READY!', font='standard'), 'blue')
