import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from datetime import datetime
from source.bot.utils import CogAlert, RaiseDBError, BaseEmbed, TimeToBirthdate

class ShowBirthday(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def showbirthday(self, ctx, *, name: str):
        try:
            user_id = int(ctx.author.id)
            result = supabase.from_("birthdays").select('*').eq('user_id', user_id).execute()
            print(result)
            user = await self.client.fetch_user(user_id)
            bday = result.data[0]['birthday']
            await BaseEmbed(ctx, f'{user.name} birthday is on {TimeToBirthdate(bday)}')
            CogAlert(ctx.author.name)
        except Exception as e:
            await RaiseDBError(ctx, e)
            
async def setup(client):
    cog = ShowBirthday(client)
    await client.add_cog(cog)
