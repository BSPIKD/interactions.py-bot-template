import os
import io
from pathlib import Path
from datetime import datetime

import interactions
from termcolor import cprint
import src.services.rights as _r
from pyfiglet import figlet_format
import src.models.base_db_script as _base

import config.conf as _c


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
    return get_dir_files(_c.MASTER_MIGRATION, '.sql')


def get_server_migration_files():
    return get_dir_files(_c.SERVER_MIGRATION, '.sql')


def parse_cmd_name(cmd: str):
    return cmd.replace(' ', '-')


def get_unix_timestamp():
    return int(datetime.now().timestamp());


def print_info():
    cprint(figlet_format('Author', font='larry3d'), 'cyan')
    cprint(figlet_format(_c.__author__, font='standard'), 'red')
    cprint(figlet_format('Bot', font='larry3d'), 'cyan')
    cprint(figlet_format(f'{_c.__name__} v{_c.__version__}', font='standard'), 'red')
    cprint(figlet_format('--------', font='larry3d'), 'blue')
    cprint(figlet_format('BOT IS READY!', font='standard'), 'blue')


async def send_msg_to_cnl(client, cnl_id: int, msg: str):
    channel = await client._http.get_channel(cnl_id)  # Todo: TO LIVE
    channel = interactions.Channel(**channel, _client=client._http)
    await channel.send(msg)


async def send_embed_to_cnl(client, cnl_id: int, embed: str):
    channel = await client._http.get_channel(cnl_id)
    channel = interactions.Channel(**channel, _client=client._http)
    await channel.send(embeds=embed)


async def send_msg_embed_to_cnl(client, cnl_id: int, msg: str, embed: str):
    channel = await client._http.get_channel(cnl_id)
    channel = interactions.Channel(**channel, _client=client._http)
    await channel.send(msg, embeds=embed)


async def server_log_msg(client, db: int, msg: str):
    await send_msg_to_cnl(client, int(_base.get_config(_c.cnl_log, db)), msg)


async def server_log_embed(client, db: int, embed):
    await send_embed_to_cnl(client, int(_base.get_config(_c.cnl_log, db)), embed)


async def server_log_msg_embed(client, db: int, msg: str, embed):
    await send_msg_embed_to_cnl(client, int(_base.get_config(_c.cnl_log, db)), msg, embed)


async def get_channel(client, cnl_id):
    channel = await client._http.get_channel(cnl_id)
    channel = interactions.Channel(**channel, _client=client._http)
    return channel


async def are_configs_set(ctx):
    """
    Check config set
    :param ctx: interactions.CommandContext or interactions.Channel
    :return:
    """
    cf = _r.get_and_check_unset_config(int(ctx.guild_id))
    if not cf[0]:
        await ctx.send(cf[1])
        return False
    return True
