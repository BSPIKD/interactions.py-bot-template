import interactions

import src.models.base_db_script as _base
import src.services.db_manager as dbs
import config.conf as _c


async def check_cmd_rights(ctx: interactions.CommandContext, cmd_name: str, author: interactions.Member, db: int):
    right = _base.get_cmd_rights(cmd_name, db)
    if right == 'SU':
        return await is_user_su(ctx)
        # if int(author.id) == int(_base.get_config(_c.super_user, db)):
        #     return True
        # await ctx.send(_c.err_msg_no_rights, ephemeral=True)
        # return False
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
    cmd = _base.__get_cmd_by_name(cmd_name, db)
    if cmd[0] is False:
        await ctx.send('Příkaz není ještě povolený pro užívání!', ephemeral=True)
        return False
    elif cmd[0] is True and cmd[1] is False:
        await ctx.send('Příkaz je vypnutý!', ephemeral=True)
        return False
    return True  # CMD is on and allowed


async def are_configs_set(ctx: interactions.CommandContext, db: int):
    config_set = _base.__get_count_of_unset_configs(int(ctx.guild_id))
    if config_set[0] is False:
        msg = ''
        for c in config_set[1]:
            msg += f'Není nastaven config `{c[0]}`\n'
            print(f'Není nastaven config {c[0]}')
        await ctx.send(msg, ephemeral=True)
        return False
    return True


async def is_user_su(ctx: interactions.CommandContext):
    await ctx.get_guild()
    if int(ctx.author.id) != int(ctx.guild.owner_id):
        await ctx.send("Nejsi zakladatel!")
        return False
    return True
