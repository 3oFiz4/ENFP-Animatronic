For collaborators! To create a command. You should follow this Template! The variable in [] means it's optional, and depends on you.

```python
import discord
from discord.ext import commands

class [COMMAND_NAME](commands.Cog):
    def __init__(self, client):
        self.client = client #! Do not remove  this.
        # You can add more variables if you want. 

    @commands.command()
    async def [COMMAND_NAME](self, ctx):
        # Add your code here...
        await ctx.send('Pong!') # This is a example script. You can create your own if you want.

# The set-up for the cog command.
async def setup(client):
    await client.add_cog([COMMAND_NAME](client))
```
