
# === MODULE START === #
import discord 
import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio as io
import json
from rich import print as log
import concurrent.futures
# === MODULE END === #
with open("../config.json") as f:config = json.load(f)
intents=discord.Intents.default()
intents.message_content = True
Host = commands.Bot(command_prefix=config["COMMAND_PREFIX"], intents=intents)
load_dotenv()  # Retrieve environment variables from .env.
TOKEN = os.getenv("YOUR_BOT_ACCOUNT_TOKEN")

# Simply tell the USER if the Bot are ready or not.
@Host.event
async def on_ready():
    log(f'''[cyan bold]BEGIN[/cyan bold]
[cyan]Logged in as: [lime]{Host.user.name} ({Host.user.id})[/lime][/cyan]
[blue]Discord.py Version: {discord.__version__}[/blue]''')
    await Host.change_presence(activity=discord.Game(name=config['ON_READY']['PRESENCE_MESSAGE']))

# Walk through the `cogs` folder, and for every sub-directory, if there is a .py format file, will be load the Cogs.
@Host.event
async def setup_hook():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    cogs_dir = os.path.join(main_dir, 'cogs')

    async def load_extension(module):
        await Host.load_extension(module)
        log(f"[cyan bold]COG LOADED[/] [purple]{module}[/]")

    tasks_load = [load_extension(os.path.join(root, file).replace(os.sep, '.')[len(main_dir)+1:-3])
             for root, dirs, files in os.walk(cogs_dir) 
             for file in files if file.endswith('.py')]

    await io.gather(*tasks_load)


# Run the token.
Host.run(TOKEN)    
