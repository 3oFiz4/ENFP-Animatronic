import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from source.bot.utils import CogAlert, BaseEmbed, RaiseDBError, TimeToBirthdate
from inspect import getmembers, isclass
from sys import modules

class ListBirthday(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def listbirthday(self, ctx):
        try:
            bday_list = ''
            result = supabase.from_("birthdays").select('*').order("birthday").execute()
            if result:
                for birthday in result.data:
                    bday = birthday['birthday']
                    uid = birthday['user_id']
                    user = await self.client.fetch_user(uid)
                    bday_list += f"> **Username**: {user.mention}\n> **Birthday**: {TimeToBirthdate(bday)}\n\n\n"
                    print(bday)
                await BaseEmbed(ctx, 'Upcoming birthday!', bday_list)
                CogAlert(ctx.author.name)
            else:
                await ctx.send('No upcoming birthdays.')
        except Exception as e:
            await RaiseDBError(ctx, e)
            
async def setup(client):
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))
