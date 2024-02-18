from discord.ext import commands
from source.bot.utils import BaseEmbed
from inspect import getmembers, isclass
from sys import modules

class Say(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def say(self, ctx, channel_id:int, *, message):
        target_channel = self.client.get_channel(channel_id)
        if target_channel is not None:
            await target_channel.send(message)
        else:
            await ctx.send('Cannot be found')

async def setup(client):
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))