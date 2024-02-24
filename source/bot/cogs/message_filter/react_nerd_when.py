from discord.ext import commands
from source.bot.utils import BaseEmbed, CogAlert
import re
from inspect import getmembers, isclass
from sys import modules

class ReactNerd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if re.search(r'\bActually\b', message.content, re.IGNORECASE):
            await message.add_reaction('🤓')

async def setup(client):
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))