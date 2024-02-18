from discord.ext import commands
from source.bot.utils import CogAlert
from inspect import getmembers, isclass
from sys import modules

class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clear(self, ctx, amount=5):
        amount += 1
        await ctx.channel.purge(limit=amount)
        CogAlert(ctx.author.name)
        
    #! THIS IS EXCLUSIVE, MEANING THAT IT WILL STOP DELETING MESSAGES, WHEN THE MESSAGE_ID ARE SAME TO THE MESSAGE.
    @commands.command()
    async def clear_until(self, ctx, message_id):
        channel = ctx.channel
        msg = await channel.fetch_message(message_id)
        await channel.purge(after=msg, oldest_first=False)
        CogAlert(ctx.author.name)

async def setup(client):
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))