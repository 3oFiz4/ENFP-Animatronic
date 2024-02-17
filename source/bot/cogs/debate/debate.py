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
        self.sealed = False
        
    @commands.Cog.listener()
    async def on_message(self, ctx):
        try:
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
        except Exception as e:
            pass

    @commands.command()
    async def topic(self, ctx, *, topic: str):
        self.debate_topic = topic
        self.participants = []
        self.turn = 0
        self.locked = True
        self.sealed = False
        await BaseEmbed(ctx, f'A new debate on "{topic}" has started!', Desc=f'Use `{config["COMMAND_PREFIX"]}join` to participate.')
        CogAlert(f"{ctx.author.name} (TOPIC: {topic})")
    
    @commands.command()
    async def join(self, ctx):
        if self.locked and not self.sealed and ctx.author not in self.participants:
            self.participants.append(ctx.author)
            await BaseEmbed(ctx, f'{ctx.author.name} joined the debate.')
        else:
            await BaseEmbed(ctx, 'You have already joined the debate, no debate has started, or the debate is sealed.', Color=(255,0,0))
    
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
    async def seal(self, ctx):
        if ctx.author == self.participants[0]:
            self.sealed = True
            await BaseEmbed(ctx, 'Debate sealed!', 'The debate has been sealed. No more participants can join.')
        else:
            await BaseEmbed(ctx, 'Insufficient permission', 'Only the user who started the debate can seal it.', Color=(255,0,0))

    @commands.command()
    async def unseal(self, ctx):
        if ctx.author == self.participants[0]:
            self.sealed = False
            await BaseEmbed(ctx, 'Debate unsealed!', 'The debate has been unsealed. Any participants can join now.')
        else:
            await BaseEmbed(ctx, 'Insufficient permission', 'Only the user who started the debate can unseal it.', Color=(255,0,0))

    @commands.command()
    async def end(self, ctx):
        self.debate_topic = ''
        self.participants = []
        self.turn = 0
        self.locked = False
        self.sealed = False
        await BaseEmbed(ctx, "Debate ended.", Desc=f"Ended by {ctx.author.mention}", Color=(255,0,0))
    
    @commands.command()
    async def helpdebate(self, ctx):
        await BaseEmbed(ctx, "How to use `Debate bot`?", Desc=f"""
## Before starting:
1. Both participants should be agreed to continue the debate in here.
2. Both participants have a topic to talk about.
3. Read rules.

## How to run the command:
1. Run ``;topic [TOPIC:str]`, *note that: The first user who run the command will be the one who speak first*. Let's say you want to debate about "Why US's human rights is collapsed", you can run.
`;topic Why US's human rights is collapsed`
2. Upon trigger the command, both participant should join, by trigger the command. `;join`. So you trigger `;join`, and then another user should trigger `;join`
3. Since the one who run the `;topic` gets to talk first, and assuming you done with your rant, you can let other participant speak by trigger the command `;pass`, this also applied when another participants done with their rant.
4. If you do not wanting any member to participate the debate, you can run `;seal`. Otherwise, if you have run `;seal` before, and you want anyone to participate, you can run `;unseal`
5. To end the debate, both participants should agreed, and any participant can trigger `;end` to end a debate.
""", Color=(0,255,0))
        
async def setup(client):
    await client.add_cog(Debate(client))