import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory
from datetime import datetime
from source.bot.utils import CogAlert, BaseEmbed, RaiseDBError, RaiseParamError

class RemoveNote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def removenote(self, ctx, *, id: int = None):
        error = await RaiseParamError(self.removenote, ctx=ctx, id=id)
        try:
            now = datetime.now()
            now_str = now.strftime('%d/%m/%Y %H:%M:%S')  # Format the datetime object to a string
            result = supabase.table("Notes").delete().eq('id', id).execute()
            await BaseEmbed(ctx, 'Note updated!', f'The note with ID {id} removed at ({now_str})')
            CogAlert(ctx.author.name)
        except Exception as e:
            await RaiseDBError(ctx, e)

async def setup(client):
    await client.add_cog(RemoveNote(client))