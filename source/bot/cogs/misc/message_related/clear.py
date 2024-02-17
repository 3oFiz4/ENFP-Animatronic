
import discord
from discord.ext import commands
from source.bot.utils import BaseEmbed, CogAlert
import hashlib, itertools
class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clear(self, ctx, amount=5):
        amount += 1
        await ctx.channel.purge(limit=amount)
        
    #! THIS IS EXCLUSIVE, MEANING THAT IT WILL STOP DELETING MESSAGES, WHEN THE MESSAGE_ID ARE SAME TO THE MESSAGE.
    @commands.command()
    async def clear_until(self, ctx, message_id):
        channel = ctx.channel
        msg = await channel.fetch_message(message_id)
        await channel.purge(after=msg, oldest_first=False)

async def setup(client):
    await client.add_cog(Clear(client))