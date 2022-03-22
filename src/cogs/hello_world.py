import interactions


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
    async def hello_world(self, ctx, sub_command: str):
        """
        Ukázka příkazu pomocí cogs
        :param ctx: Context
        :param sub_command: Pod příkaz
        """
        # Todo: Napsat metodu pro logování
        await ctx.send(f"Hello, World! - {sub_command}")


def setup(client):
    HelloWorld(client)
