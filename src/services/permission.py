import interactions
import config.conf as _c

from src.models.base_db import BaseDb


class Perms:
    def __init__(self, database: int):
        self.base = BaseDb(database=database)

    async def check_cmd_rights(self, ctx: interactions.CommandContext, cmd_name: str, author: interactions.Member):
        right = self.base.get_cmd_rights(cmd_name)
        if right == 'SU':
            return await self.is_user_su(ctx)
            # if int(author.id) == int(_base.get_config(_c.super_user, db)):
            #     return True
            # await ctx.send(_c.err_msg_no_rights, ephemeral=True)
            # return False
        if right == 'SS':
            # check if user have OWNER role
            r = int(self.base.get_config(_c.role_owner))
            if r in author.roles:
                return True
            await ctx.send(_c.err_msg_no_rights, ephemeral=True)
            return False
        elif right == 'S':
            # check if user have MAIN ADMIN or OWNER role
            if not int(self.base.get_config(_c.role_owner)) in author.roles:
                if not int(self.base.get_config(_c.role_main_admin)) in author.roles:
                    await ctx.send(_c.err_msg_no_rights, ephemeral=True)
                    return False
                return True
            else:
                return True
        elif right == 'AA':
            # check if user have ADMIN, MAIN ADMIN or OWNER role
            if not int(self.base.get_config(_c.role_owner)) in author.roles:
                if not int(self.base.get_config(_c.role_main_admin)) in author.roles:
                    if not int(self.base.get_config(_c.role_admin)) in author.roles:
                        await ctx.send(_c.err_msg_no_rights, ephemeral=True)
                        return False
                    return True
                return True
            else:
                return True
        elif right == 'A':
            # check if user have ATEAM role
            r = int(self.base.get_config(_c.role_ateam))
            if r in author.roles:
                return True
            await ctx.send(_c.err_msg_no_rights, ephemeral=True)
            return False
        elif right == 'U':
            return True
        await ctx.send(_c.err_msg_no_rights, ephemeral=True)
        return False

    async def is_user_su(self, ctx: interactions.CommandContext):
        await ctx.get_guild()
        if int(ctx.author.id) != int(ctx.guild.owner_id) or int(ctx.author.id) != int(_c.__author_id__):
            await ctx.send("Nejsi zakladatel!")
            return False
        return True

    async def is_cmd_exist_or_allowed(self, ctx: interactions.CommandContext, cmd_name: str):
        """
        Zkontroluje zda je příkaz zavedený v databázi, povolený, nebo vypnutý
        :param ctx: context
        :param cmd_name: Cmd Name
        :return: tuple[bool, bool] [False, False] -> cmd off production, [True, False] -> cmd is turn of, [True, True] -> cmd is on
        """
        cmd = self.base.get_cmd_by_name(cmd_name)
        if cmd[0] is False:
            await ctx.send('Příkaz není ještě povolený pro užívání!', ephemeral=True)
            return False
        elif cmd[0] is True and cmd[1] is False:
            await ctx.send('Příkaz je vypnutý!', ephemeral=True)
            return False
        return True  # CMD is on and allowed

    def get_and_check_unset_config(self):
        config_set = self.base.get_count_of_unset_configs()
        if config_set[0] is False:
            msg = ''
            for c in config_set[1]:
                msg += f'Není nastaven config `{c[0]}`\n'
                print(f'Není nastaven config {c[0]}')
            return False, msg
        return True, None
