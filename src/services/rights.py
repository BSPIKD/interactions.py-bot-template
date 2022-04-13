import interactions

import src.models.base_db_script as _base
import src.services.db_manager as dbs
import config.conf as _c


async def check_cmd_rights(ctx: interactions.CommandContext, cmd_name: str, author: interactions.Member, db: int):
    right = get_cmd_rights(cmd_name, db)
    if right == 'SU':
        if int(author.id) == int(_base.get_config(_c.super_user, db)):
            return True
        await ctx.send(_c.err_msg_no_rights, ephemeral=True)
        return False
    if right == 'SS':
        # check if user have OWNER role
        r = int(_base.get_config(_c.role_owner, db))
        if r in author.roles:
            return True
        await ctx.send(_c.err_msg_no_rights, ephemeral=True)
        return False
    elif right == 'S':
        # check if user have MAIN ADMIN or OWNER role
        if not int(_base.get_config(_c.role_owner, db)) in author.roles:
            if not int(_base.get_config(_c.role_main_admin, db)) in author.roles:
                await ctx.send(_c.err_msg_no_rights, ephemeral=True)
                return False
            return True
        else:
            return True
    elif right == 'AA':
        # check if user have ADMIN, MAIN ADMIN or OWNER role
        if not int(_base.get_config(_c.role_owner, db)) in author.roles:
            if not int(_base.get_config(_c.role_main_admin, db)) in author.roles:
                if not int(_base.get_config(_c.role_admin, db)) in author.roles:
                    await ctx.send(_c.err_msg_no_rights, ephemeral=True)
                    return False
                return True
            return True
        else:
            return True
    elif right == 'A':
        # check if user have ATEAM role
        r = int(_base.get_config(_c.role_ateam, db))
        if r in author.roles:
            return True
        await ctx.send(_c.err_msg_no_rights, ephemeral=True)
        return False
    elif right == 'U':
        return True
    await ctx.send(_c.err_msg_no_rights, ephemeral=True)
    return False


# ===================================== MODEL
async def is_cmd_exist_or_allowed(ctx: interactions.CommandContext, cmd_name: str, db: int):
    """
    Zkontroluje zda je příkaz zavedený v databázi, povolený, nebo vypnutý
    :param ctx: context
    :param cmd_name: Cmd Name
    :param db: Guild ID
    :return: tuple[bool, bool] [False, False] -> cmd off production, [True, False] -> cmd is turn of, [True, True] -> cmd is on
    """
    cmd = __get_cmd_by_name(cmd_name, db)
    if cmd[0] is False:
        await ctx.send('Příkaz není ještě povolený pro užívání!', ephemeral=True)
        return False
    elif cmd[0] is True and cmd[1] is False:
        await ctx.send('Příkaz je vypnutý!', ephemeral=True)
        return False
    return True  # CMD is on and allowed


def __get_cmd_by_name(cmd_name: str, db: int):
    """
    Check if command exist in database
    :param cmd_name:
    :param db:
    :return:
    """
    with dbs.Connection(db) as conn:
        sql = f"select * from config_cmds where name = ?"
        conn.cur.execute(sql, (cmd_name,))
        data = conn.cur.fetchone()
        if data is None:
            return False, False  # Neexistuje
        else:
            if int(data[3]) == 1:
                return True, True  # Existuje a je zapnutý
            return True, False  # Existuje a je vypnutý


def __get_count_of_unset_configs(db: int):
    with dbs.Connection(db) as conn:
        sql = f"select * from config where is_important = 1 and value is null"
        conn.cur.execute(sql)
        rows = conn.cur.fetchall()
        if len(rows) > 0:
            return False, rows
        return True, None


async def are_configs_set(ctx: interactions.CommandContext, db: int):
    config_set = __get_count_of_unset_configs(int(ctx.guild_id))
    if config_set[0] is False:
        msg = ''
        for c in config_set[1]:
            msg += f'Není nastaven config `{c[0]}`\n'
            print(f'Není nastaven config {c[0]}')
        await ctx.send(msg, ephemeral=True)
        return False
    return True


def get_cmd_rights(cmd_name: str, db: int):
    """
    Get commands user rights by command name
    :param cmd_name:
    :param db:
    :return:
    """
    with dbs.Connection(db) as conn:
        sql = f"select rights from config_cmds where name = ?"
        conn.cur.execute(sql, (cmd_name,))
        return conn.cur.fetchone()[0]
