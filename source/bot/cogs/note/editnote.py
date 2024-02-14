import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from datetime import datetime

class EditNote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def editnote(self, ctx, id: int, *, new_content: str):
        try:
            now = datetime.now()
            now_str = now.strftime('%d/%m/%Y %H:%M:%S')  # Format the datetime object to a string
            result = supabase.table("Notes").update({"content": new_content, "updated_at": now.isoformat()}).eq('id', id).execute()
            await ctx.send(f"The note with ID {id} updated to ({now_str}): {new_content}")
        except Exception as e:
            if str(e) == 'Database offline':
                await ctx.send("Sorry. The database currently is offline. You can ping the author of this bot, for further information.\nMost of the time when the database is offline, because the author shut it down.")

async def setup(client):
    await client.add_cog(EditNote(client))