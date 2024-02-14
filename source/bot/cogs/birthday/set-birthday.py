import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from datetime import datetime

class SetBirthday(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setbirthday(self, ctx, *, date: str):
        try:
            birthday = datetime.strptime(date, '%d-%m-%Y').date()

            # Insert or update the birthday in the database
            user_id = str(ctx.author.id)
            result = supabase.table("birthdays").insert({"user_id": user_id, "birthday": birthday.isoformat()}).execute()
            if result:
                await ctx.send(f'Birthday set to {birthday}!')
        except Exception as e:
            if str(e) == 'Database offline':
                await ctx.send("Sorry. The database currently is offline. You can ping the author of this bot, for further information.\nMost of the time when the database is offline, because the author shut it down.")
            else:
                print(e)

async def setup(client):
    await client.add_cog(SetBirthday(client))
