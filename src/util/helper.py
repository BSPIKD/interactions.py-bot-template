import os
import io
from pathlib import Path
from datetime import datetime

import interactions
from interactions import Member
from termcolor import cprint
from pyfiglet import figlet_format
from src.services.permission import Perms
from src.models.base_db import BaseDb
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
    return int(datetime.now().timestamp())


def print_info():
    cprint(figlet_format('Author', font='larry3d'), 'cyan')
    cprint(figlet_format(_c.__author__, font='standard'), 'red')
    cprint(figlet_format('Bot', font='larry3d'), 'cyan')
    cprint(figlet_format(f'{_c.__name__} v{_c.__version__}', font='standard'), 'red')
    cprint(figlet_format('--------', font='larry3d'), 'blue')
    cprint(figlet_format('BOT IS READY!', font='standard'), 'blue')


async def send_msg_to_cnl(client, cnl_id: int, msg: str):
    # Todo: CRITICAL - když není nastaven config neposílat!
    try:
        channel = await client._http.get_channel(cnl_id)  # Todo: TO LIVE
        channel = interactions.Channel(**channel, _client=client._http)
        await channel.send(msg)
    except TypeError:
        cprint('Nejspíš není nastaven správně config!', 'red')


async def send_embed_to_cnl(client, cnl_id: int, embed):
    channel = await client._http.get_channel(cnl_id)
    channel = interactions.Channel(**channel, _client=client._http)
    await channel.send(embeds=embed)


async def send_msg_embed_to_cnl(client, cnl_id: int, msg: str, embed):
    channel = await client._http.get_channel(cnl_id)
    channel = interactions.Channel(**channel, _client=client._http)
    await channel.send(msg, embeds=embed)


async def server_log_msg(client, db: int, msg: str):
    base = BaseDb(database=db)
    await send_msg_to_cnl(client, int(base.get_config(_c.cnl_log)), msg)


async def server_log_embed(client, db: int, embed):
    base = BaseDb(database=db)
    await send_embed_to_cnl(client, int(base.get_config(_c.cnl_log)), embed)


async def server_log_msg_embed(client, db: int, msg: str, embed):
    base = BaseDb(database=db)
    await send_msg_embed_to_cnl(client, int(base.get_config(_c.cnl_log)), msg, embed)


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
    perms = Perms(database=int(ctx.guild_id))
    cf = perms.get_and_check_unset_config()
    if not cf[0]:
        await ctx.send(cf[1])
        return False
    return True


async def add_role(client, uid: int, role_id: int, db: int):
    _member = await client._http.get_member(guild_id=db, member_id=uid)
    member = Member(**_member, _client=client._http)
    await member.add_role(
        guild_id=db,
        role=role_id)


async def remove_role(client, uid: int, role_id: int, db: int):
    _member = await client._http.get_member(guild_id=db, member_id=uid)
    member = Member(**_member, _client=client._http)
    await member.remove_role(
        guild_id=db,
        role=role_id)


def get_today() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str, db: int, color='yellow'):
    base = BaseDb(database=db)
    # Todo: nějak ukládat do global current db
    if int(base.get_config(_c.PRINT_DEBUG)) == 1:
        if int(base.get_config(_c.PRINT_HIGHLIGHT)) == 1:
            # print(f'\033[96m{get_today()} {msg} \033[0m')
            cprint(f'{get_today()} {msg}', color)
        else:
            print(f'{get_today()} {msg}')
