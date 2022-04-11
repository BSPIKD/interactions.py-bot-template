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
        cmd_name = f'hello-{sub_command}'

        if r.check_cmd_rights(cmd_name, ctx.author, int(ctx.guild_id)) is False:
            await ctx.send('Nemáte dostatečná práva pro tento příkaz!', ephemeral=True)
            return


        # Todo:
        #  Zjistit správnost kanálu

        await ctx.send(f"Hello, World! - {sub_command}")


def setup(client):
    HelloWorld(client)
