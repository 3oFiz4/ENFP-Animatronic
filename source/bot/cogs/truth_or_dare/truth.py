import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from source.bot.utils import CogAlert, BaseEmbed, RaiseDBError
from inspect import getmembers, isclass
from sys import modules
from random import randint

class Truth(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def truth(self, ctx, id=None):
        # Randomizer
        def r(length):
            return randint(0, length-1)
        truth = supabase.from_("tod").select('*').eq('type', 'Truth').execute()
        length = len(truth.data)
        if not id:
            pick = r(length)
            data = truth.data[pick]
            embed = await BaseEmbed(ctx, 'Truth', data['challenge'], field=[
                {'name': "Truth ID: ", 'value': data['id'], 'inline': True}
            ])
        else:
            data = truth.data
            pick = int(id)
            # Showcasing O(n) time complexity
            data = {i['id']: i['challenge'] for i in data}
            if pick not in data:
                return await BaseEmbed(ctx, 'Expected ID is out of range.', Color=(255,0,0))
            print(data)
            embed = await BaseEmbed(ctx, 'Truth', data.get(pick), field=[
                {'name': "Truth ID: ", 'value': pick, 'inline': True}
            ])

async def setup(client):
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))