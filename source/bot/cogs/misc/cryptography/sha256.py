import discord
from discord.ext import commands
from source.bot.utils import BaseEmbed, CogAlert
import hashlib, itertools
class SHA256Crypt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def texttosha256(self, ctx, *, text: str):
        text_bytes = text.encode()
        h_bytes = hashlib.sha256(text_bytes).digest()
        h_hex = h_bytes.hex()
        await BaseEmbed(ctx, 'Encrypted', f'**Encrypted text:**\n{text}')
        CogAlert(ctx.author.name)

async def setup(client):
    await client.add_cog(SHA256Crypt(client))