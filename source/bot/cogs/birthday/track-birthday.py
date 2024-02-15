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
from source.bot.utils import TaskAlert
import json

with open("../config.json") as f:config = json.load(f)

class CheckBirthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.task_check_birthdays())

    async def task_check_birthdays(self):
        while True:
            today = datetime.now().strftime('%d-%m')  # Get today's date as a 'dd-mm' string
            result = supabase.from_("birthdays").select("user_id").eq("birthday", today).execute()
            birthdays = [row['user_id'] for row in result.data]
            channel = await self.bot.fetch_channel(config['BIRTHDAY']['BIRTHDAY_ANNOUCE_CHANNEL'])  # This channel inside will be changed.
            for user_id in birthdays:
                user = await self.bot.fetch_user(int(user_id))
                if user:
                    await channel.send(config['BIRTHDAY']['BIRTHDAY_ANNOUNCE_MESSAGE'].format(birthday_user=user.mention))
            # Wait for 24 hours (86400 seconds) before checking again
            TaskAlert(self.task_check_birthdays)
            await io.sleep(86400)

async def setup(client):
    cog = CheckBirthday(client)
    await client.add_cog(cog)
