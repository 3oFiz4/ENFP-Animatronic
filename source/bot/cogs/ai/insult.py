import os
import sys
import openai as ai
from dotenv import load_dotenv
from discord.ext import commands
from rich import print as log
from inspect import getmembers, isclass
from sys import modules
load_dotenv()

# Load these once when your bot starts up
ai.api_key = os.getenv("AI_API_KEY")
ai.api_base = os.getenv("AI_API_BASE")
ai_model = os.getenv("AI_MODEL")

project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.bot.utils import CogAlert

class Insult(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def insult(self, ctx, *, user):
        user = await self.client.fetch_user(int(user[2:-1]))
        name = user.name
        glob_name = user.display_name
        try:
            completion = ai.ChatCompletion.create(
                model=ai_model,
                messages=[
                    {"role": "system"
                    },
                    {"role": "user", "content": f"Give an insult to {name}"}
                ]
            )
            
            r = completion.choices[0].message['content']
            
            await ctx.reply(r)
            CogAlert(ctx.author.name)
            log(f'[cyan bold]USER QUESTION: [blue]{user}[blue][/cyan bold]\nAI REPLY: [green bold]{r}[/green bold]')
        except Exception as ERR:
            log(f'[red bold]Insult Command failed to run.\nERR: {ERR}[/]\n[#FFFF00]Have you provided a correct API Endpoint and API key?[/]')

async def setup(client):
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))