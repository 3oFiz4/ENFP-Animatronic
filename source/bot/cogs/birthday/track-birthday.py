import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from datetime import datetime
import asyncio as io

class CheckBirthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.check_birthdays())

    async def check_birthdays(self):
        while True:
            today = datetime.now().date()
            result = supabase.from_("birthdays").select("user_id").eq("birthday", today).execute()
            birthdays = [row['user_id'] for row in result.data]
            channel = await self.bot.fetch_channel(1207277637395939388)  # This channel inside will be changed.
            print(birthdays)
            for user_id in birthdays:
                user = await self.bot.fetch_user(int(user_id))
                if user:
                    await channel.send(f'Say happy Birthday, to our dear friend {user.mention}! 🎉')

            # Wait for 24 hours (86400 seconds) before checking again
            await io.sleep(86400)

async def setup(client):
    await client.add_cog(CheckBirthday(client))
