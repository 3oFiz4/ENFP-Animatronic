import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.data.db import supabase  # Knowing that db.py is in the source/data directory

class ListNote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def listnote(self, ctx):
        try:
            result = supabase.from_("Notes").select('*').eq('user_id', int(ctx.author.id)).execute()
            print(result)
            notes = result.data
            notes_str = ""
            for note in notes:
                # Parsing date to desired format.
                created_at_str = note['created_at']
                updated_at_str = note['updated_at']
                if note['created_at'] is not None:
                    created_at = datetime.strptime(note['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
                    created_at_str = created_at.strftime('%d/%m/%Y %H:%M:%S')
                if note['updated_at'] is not None:
                    updated_at = datetime.strptime(note['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
                    updated_at_str = updated_at.strftime('%d/%m/%Y %H:%M:%S')
                notes_str += f"> **Note ID**: {note['id']}\n> **Content**: {note['content']}\n> **Created at**: {created_at_str}\n> **Updated at**: {updated_at_str}\n\n"
            try:
                await ctx.send(notes_str)
            except Exception as e:
                print(f"An error occurred: {e}")
        except Exception as e:
            if str(e) == 'Database offline':
                await ctx.send("Sorry. The database currently is offline. You can ping the author of this bot, for further information.\nMost of the time when the database is offline, because the author shut it down.")


async def setup(client):
    await client.add_cog(ListNote(client))