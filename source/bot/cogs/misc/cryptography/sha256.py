from discord.ext import commands
from source.bot.utils import BaseEmbed, CogAlert
import hashlib
from inspect import getmembers, isclass
from sys import modules

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
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))