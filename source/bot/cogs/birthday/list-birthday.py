import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
from discord import Embed
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from datetime import datetime

class ListBirthday(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def listbirthday(self, ctx):
        try:
            result = supabase.table('birthdays').select('*').order('birthday').limit(10).execute()
            if result:
                # TODO: Hey, dedrakenkeizer. Mind fix this? I don't have time to do so!
                # TODO: I want you to create an embed listing the user and the user birthday!
                # TODO: Example, @Nakiwa on (03-03-2024), @DeDraken on (23-12-2024)
                # TODO: The bug lies on the birthdays_str. Hope you can fix it :D! Feel free to call me out if you need some help.
                # TODO: If you have finally fix it. Clear this TODO comment.
                # Construct a string with all the birthdays
                birthdays_str = '\n'.join(f"{b[0]} on ({b[1]})" for b in result)

                # Create an embed with the birthdays string
                embed = Embed(title="Upcoming Birthdays", description=birthdays_str, color=0x00ff00)

                await ctx.send(embed=embed)
            else:
                await ctx.send('No upcoming birthdays.')
        except Exception as e:
            if str(e) == 'Database offline':
                await ctx.send("Sorry. The database currently is offline. You can ping the author of this bot, for further information.\nMost of the time when the database is offline, because the author shut it down.")
            else:
                print(e)

async def setup(client):
    await client.add_cog(ListBirthday(client))
