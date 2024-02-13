
# === MODULE START === #
import discord 
import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio as io
# === MODULE END === #
intents=discord.Intents.default()
intents.message_content = True
Host = commands.Bot(command_prefix=">", intents=intents)

load_dotenv()  # Retrieve environment variables from .env.

TOKEN = os.getenv("YOUR_BOT_ACCOUNT_TOKEN")

# Simply tell the USER if the Bot are ready or not.
@Host.event
async def on_ready():
    print('Bot ready.')

# Walk through the `cogs` folder, and for every sub-directory, if there is a .py format file, will be load the Cogs.
@Host.event
async def setup_hook():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cogs_dir = os.path.join(root_dir, 'cogs')
    for root, dirs, files in os.walk(cogs_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                module = path.replace(os.sep, '.')[len(root_dir)+1:-3]
                await Host.load_extension(module)
                print(f"Cog load: {module}")
            else:
                print("Pycache failed to load.")

# Run the token.
Host.run(TOKEN)    
