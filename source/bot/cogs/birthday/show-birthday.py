import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from datetime import datetime

class ShowBirthday(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def showbirthday(self, ctx, *, date: str):
        try:
            # TODO: Hey, dedrakenkeizer. Fix this one please.
            # TODO: I want you to show the user birthday.
            # TODO: The bug lies on the await ctx.send(f'{user.mention} birthday is on {result['birthday']}')
            # TODO: If you have finally fix it. Clear this TODO comment.
            user_id = int(ctx.author.id)
            result = supabase.from_("birthdays").select('*').eq('user_id', user_id).execute()
            if result:
                user = await self.bot.fetch_user(user_id)
                await ctx.send(f'{user.mention} birthday is on {result['birthday']}')
        except Exception as e:
            if str(e) == 'Database offline':
                await ctx.send("Sorry. The database currently is offline. You can ping the author of this bot, for further information.\nMost of the time when the database is offline, because the author shut it down.")
            else:
                print(e)

async def setup(client):
    await client.add_cog(ShowBirthday(client))
