import interactions

# import src.services.rights as _r
import src.util.helper as _h

from src.services.permission import Perms


class HelloWorld(interactions.Extension):
    """
    Ukázkový cog příkaz
    """
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name="hello",
        description="Print hello world",
        options=[
            interactions.Option(
                name="world",
                description="Print hello world",
                type=interactions.OptionType.SUB_COMMAND)
        ],
    )
    async def hello_world(self, ctx: interactions.CommandContext, sub_command: str):
        """
        Ukázka příkazu pomocí cogs
        :param ctx: Context
        :param sub_command: Pod příkaz
        """
        perms = Perms(database=int(ctx.guild_id))


        if await _h.are_configs_set(ctx) is False:
            return

        cmd_name = f'hello-{sub_command}'
        if await perms.is_cmd_exist_or_allowed(ctx, cmd_name) is False:
            return

        # Set command only for server owner
        # if await r.is_user_su(ctx) is False:
        #     return

        # Check the rights according to the configuration in the database
        if await perms.check_cmd_rights(ctx, cmd_name, ctx.author) is False:
            return

        # Todo:
        #  Zjistit správnost kanálu

        await ctx.send(f"Hello, World! - {sub_command}")


def setup(client):
    HelloWorld(client)
