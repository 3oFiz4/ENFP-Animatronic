import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from datetime import datetime
from source.bot.utils import CogAlert, BaseEmbed, RaiseDBError

class EditNote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def editnote(self, ctx, id: int, *, new_content: str):
        
        try:
            now = datetime.now()
            now_str = now.strftime('%d/%m/%Y %H:%M:%S')  # Format the datetime object to a string
            result = supabase.table("Notes").update({"content": new_content, "updated_at": now.isoformat()}).eq('id', id).execute()
            await BaseEmbed(ctx, 'Note updated', f"The note with ID {id} updated to ({now_str}): {new_content}")
            CogAlert(ctx.author.name)
        except Exception as e:
            await RaiseDBError(ctx, e)
            
async def setup(client):
    await client.add_cog(EditNote(client))