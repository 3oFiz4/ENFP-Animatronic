import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
from inspect import getmembers, isclass
from sys import modules

load_dotenv()

project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)

from source.data.db import supabase  # Knowing that db.py is in the source/data directory

#? From, DaemonPooling
#? This is an example command that utilize your Discord.py.
#? And btw! DeDrakenkeizer, notice the data, and error variable? That's our Database.
#? It's pretty similar somehow to SQL... just come with steroid :3
class ExampleCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def add(self, ctx, *, content: str):
        try:
            # This variable will insert any data passed to the `content` argument, into the table `Content`.
            data, error = supabase.table('Content').insert({'content': content}).execute()
        except Exception as e:
            if str(e) == 'Database offline':
                await ctx.send("Sorry. The database currently is offline. You can ping the author of this bot, for further information.\nMost of the time when the database is offline, because the author shut it down.")
            else:
                await ctx.send(f"An unexpected error occurred: {e}")

async def setup(client):
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))
