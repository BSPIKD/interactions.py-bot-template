import interactions

import src.services.rights as r


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

        if await r.are_configs_set(ctx, int(ctx.guild_id)) is False:
            return

        cmd_name = f'hello-{sub_command}'
        if await r.is_cmd_exist_or_allowed(ctx, cmd_name, int(ctx.guild_id)) is False:
            return

        # Set command only for server owner
        # if await r.is_user_su(ctx) is False:
        #     return

        # Check the rights according to the configuration in the database
        if await r.check_cmd_rights(ctx, cmd_name, ctx.author, int(ctx.guild_id)) is False:
            return

        # Todo:
        #  Zjistit správnost kanálu

        await ctx.send(f"Hello, World! - {sub_command}")


def setup(client):
    HelloWorld(client)
