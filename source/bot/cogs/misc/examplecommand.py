import discord
from discord.ext import commands
from source.bot.utils import BaseEmbed
class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await BaseEmbed(ctx, 'Hola', 'A hola message.')

async def setup(client):
    await client.add_cog(ping(client))