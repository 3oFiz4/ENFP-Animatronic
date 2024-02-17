import discord, json
from discord.ext import commands
from source.bot.utils import BaseEmbed, CogAlert

with open("../config.json") as f:config = json.load(f)

class Debate(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.debate_topic = ''
        self.participants = []
        self.turn = 0
        self.locked = False
        
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if (
            self.locked and 
            ctx.author != self.client.user and 
            not ctx.content.startswith(config["COMMAND_PREFIX"]) and
            ctx.author != self.participants[self.turn]
            ):
            await ctx.author.send(f'Please use `{config["COMMAND_PREFIX"]}join` to participate in the debate.')
            await ctx.delete()
        elif (
              not ctx.content.startswith(config["COMMAND_PREFIX"]) and 
              ctx.author != self.participants[self.turn]
            ):
            await ctx.author.send('It\'s not your turn yet.', delete_after=10)
            await ctx.delete()

    @commands.command()
    async def topic(self, ctx, *, topic: str):
        self.debate_topic = topic
        self.participants = []
        self.turn = 0
        self.locked = True
        await BaseEmbed(ctx, f'A new debate on "{topic}" has started!', Desc=f'Use `{config["COMMAND_PREFIX"]}join` to participate.')
        CogAlert(f"{ctx.author.name} (TOPIC: {topic})")
    
    @commands.command()
    async def join(self, ctx):
        if self.locked and ctx.author not in self.participants:
            self.participants.append(ctx.author)
            await BaseEmbed(ctx, f'{ctx.author.name} joined the debate.')
        else:
            await BaseEmbed(ctx, 'You have joined the debate')
    
    # btw `pass` is a used word by python syntax, thats why its _pass
    @commands.command(name='pass')
    async def _pass(self, ctx):
        if ctx.author == self.participants[self.turn]:
            self.turn = (self.turn + 1) % len(self.participants)
            await BaseEmbed(ctx, f"It's {self.participants[self.turn].name}'s turn to speak.")
        else:
            await ctx.delete()
            await ctx.author.send("Only the current speaker can pass the turn.")

    @commands.command()
    async def end(self, ctx):
        self.debate_topic = ''
        self.participants = []
        self.turn = 0
        await BaseEmbed(ctx, "Debate ended.", Desc=f"Ended by {ctx.author.mention}", Color=(255,0,0))
        
async def setup(client):
    await client.add_cog(Debate(client))