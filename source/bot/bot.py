
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

class CustomHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(title="Help", description="""
```python
    # WE ARE ASSUMING, WE ARE USING ";" AS THE COMMAND'S PREFIX
    # * means optional

    # Notes related commands:
    >addnote [TEXT:str] ## Add a note 
    >editnote [NOTE_ID:int] [TEXT:str] ## Edit a specific note id's content
    >listnote ## List your note
    >removenote [NOTE_ID:int] ## Remove a specific note id

    # Birthday related commands:
    >showbirthday [USER_ID:int] ## Show anyone's birthday
    ## e.g. `>showbirthday 901404605336916018`
    >setbirthday [DATE: Format(%d-%m)] ## Set your birthday
    ## e.g. `>setbirthday 03-03` will give 3 March
    >listbirthday ## List everyone birthday in order
    >forgetbirthday ## Remove your birthday from the D

    # Misc related commands:
    >sing [ARTIST:str] [MUSIC_NAME:str] [DELAY:int] [SING_TOGETHER: 1 | 0] ## Sing a specific song with/without a bot.
    >texttosha256 [TEXT:str] ## Encrypt text to SHA256
    >clear [NUMBER_OF_MESSAGES:int] ## Delete [NUMBER_OF_MESSAGES] above.
    >clear_until [MESSAGE:ID] ## Delete every messages, until a message with the same message_ID are found, it will stop deleting (EXCLUSIVE).
    >log_until [MESSAGE:ID] [TUPLE_LIKE_STRING]
    ## The parameter in TUPLE_LIKE_IN_STRING are below:
    ## (1st param) show_author = 1
    ## (2nd param) show_author_id = 1
    ## (3rd param) show_msg = 1
    ## (4th param) show_msg_id = 1
    ## (5th param) show_msg_created_at = 1
    ## e.g. `;log_until "1207784045661130819" "(1, 0, 1, 0, 0)" `

    # Matching related commands:
    ## discord.User is a datatype, which you can trigger using @[USERNAME]
    >ship [FIRST_USER:discord.User] [SECOND_USER:discord.User]
    ## e.g. `;ship @Nakiwa @Cleo`
    >zamn [USER:discord.User] ## Put your profile in a zamn template.... lmfao.

    # AI Related commands:
    >askenfp [TEXT:str] ## It simply give the GPT a text, which will be output to current channel.
    ## e.g. `;askenfp Why US's human rights is collapsed`

    # Debate related commands:
    >helpdebate ## Explain how to use the command. I suggest run this command first, before playing with the commands.
    >topic [TOPIC:str] ## Start a debate regarding the topic.
    # e.g. `;topic Why US's human rights is collapsed`
    >join ## Join a debate, if only the debate is unsealed.
    >pass ## Let next participant have a speak, after yours.
    >seal ## Seal the debate, so no one can join.
    >unseal ## Unseal the debate, so anyone can join. You'll use this after you `>seal` the debate. 
    >end ## End the debate.

    # Truth or Dare commands:
    >dare *[ID:int] ## Retrieve a randomized or a selected ID of a dare from the DB
    >truth *[ID:int] ## Retrieve a randomized or a selected ID of a truth from the DB
    >request [TYPE:Dare | Truth] [TEXT:str] ## Upload a Dare or Truth content to the DB
    ## e.g. `;request Dare lick a soap`
```
                          """, colour=discord.Colour.blurple())
        await destination.send(embed=e)

Host.help_command = CustomHelpCommand()

# Run the token.
Host.run(TOKEN)    
