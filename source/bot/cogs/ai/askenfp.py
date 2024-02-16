import os
import sys
import openai as ai
from dotenv import load_dotenv
from discord.ext import commands
from rich import print as log
load_dotenv()
project_root = os.getenv('PROJECT_ROOT')
sys.path.insert(0, project_root)
from source.bot.utils import CogAlert

class AskENFP(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def askenfp(self, ctx, *, text: str):
        try:
            ai.api_key = os.getenv("AI_API_KEY")
            ai.api_base = os.getenv("AI_API_BASE")
            completion = ai.ChatCompletion.create(
                model=os.getenv("AI_MODEL"),
                messages=[
                    {"role": "system", "content": 
                        "Use casual tone, short messages, irony and sarcasm if wanted."
                    },
                    {"role": "user", "content": text}
                ]
            )
            
            r = completion.choices[0].message['content']
            
            await ctx.reply(r)
            CogAlert(ctx.author.name)
            log(f'[cyan bold]USER QUESTION: [blue]{text}[blue][/cyan bold]\nAI REPLY: [green bold]{r}[/green bold]')
        except Exception as ERR:
            log(f'[red bold]AskENFP Command failed to run.\nERR: {ERR}[/]\n[#FFFF00]Have you provided a correct API Endpoint and API key?[/]')

async def setup(client):
    await client.add_cog(AskENFP(client))