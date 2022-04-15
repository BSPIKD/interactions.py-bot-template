import datetime
import logging
import os

import interactions

# import core.db.db_connector as db
from termcolor import cprint

import src.util.helper as _h
import src.services.migration as mig
from pyfiglet import figlet_format
from dotenv import load_dotenv

load_dotenv(".env")
# logging.basicConfig(level=0)
logger = logging.getLogger("Application")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(f"logs/migration_{datetime.datetime.today().timestamp()}.log")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter("%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# logger.info('info test')
# logger.warning('warning test')

bot = interactions.Client(token=os.getenv("BSPIKD_TEST"), intents=interactions.Intents.ALL)

for filename in os.listdir("./src/cogs"):
    if filename.endswith(".py"):
        bot.load(f"src.cogs.{filename[:-3]}")


@bot.event
async def on_message_create(message):
    """
    Event vykonaný při napsání nové zprávy
    :param message: Zpráva
    """
    if message.author.bot is False or message.author.bot is None:
        print(f"on_message_create - user > {message.author.username}#{message.author.discriminator}")
    else:
        print(f"on_message_create - bot > {message.author.username}#{message.author.discriminator}")


@bot.event
async def on_guild_create(guild: interactions.Guild):
    """
    Event vykonaný při přidání bota na server, provede se i když se bot zapíná
    :param guild: Discord server
    """
    cprint('==========================================================================', 'cyan')
    cprint(figlet_format('SERVER  MIGRATION', font='small'), 'cyan')
    mig.apply_server_migrations(int(guild.id), guild.name)  # Todo: SERVER MIGRACE
    print(f"on_guild_create - {guild.name}")


@bot.event
async def on_guild_delete(guild: interactions.Guild):
    """
    Event vykonaný při odstranění bota ze serveru (žádné parametry), celkem nepotřebný event
    :param guild:
    :return:
    """
    print("on_guild_delete")


@bot.event
async def on_guild_member_add(member: interactions.GuildMember):
    """
    Event vykonaný při připojení nového uživatele nebo bota na server kde je bot
    :param member: Uživatel
    """
    print(f"on_guild_member_add - {member.user.username}#{member.user.discriminator}")


@bot.event
async def on_guild_member_remove(member: interactions.GuildMember):
    """
    Event vykonaný při odstranění uživatele nebo bota se serveru (i sám sebe na serveru)
    :param member: Uživatel nebo bot
    """
    print(f"on_guild_member_remove - {member.user.username}{member.user.discriminator}")


@bot.event
async def on_message_reaction_add(message: interactions.MessageReaction):
    """
    Event vykonaný při přidání reakce
    :param message: Zpráva na které byla přidána reakce
    """
    print(f"on_message_reaction_add - {message.message_id}")


@bot.event
async def on_message_reaction_remove(message: interactions.MessageReaction):
    """
    Event vykonaný při odstranění reakce
    :param message: Zpráva na které byla odebrána reakce
    """
    print(f"on_message_reaction_remove - {message.message_id}")


@bot.event
async def on_ready():
    """
    Event vykonaný při zapnutí
    """
    _h.print_info()
    cprint('===============================================================================', 'magenta')
    cprint(figlet_format('MASTER  MIGRATION', font='small'), 'magenta')
    mig.apply_master_migrations()
    print("on_ready")

# Todo: tabulka logs a psát tam logy chyb apod

bot.start()
