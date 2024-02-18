For collaborators! To create a command. You should follow this Template! The variable in [] means it's optional, and depends on you.

The name for the command can be anything! But it has to be understandable!

```python
import discord
from discord.ext import commands
from source.bot.utils import BaseEmbed
from inspect import getmembers, isclass
from sys import modules
class [CLASS_NAME](commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        # Your code.

async def setup(client):
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))
```

UPDATE: I refactor all commands in the cog and replace this code below:
```py
async def setup(client):
    await client.add_cog([COMMAND_NAME](client))
```

WITH below, so you dont have to restate the class name. But there are other occasion where you need to apply the script above. If a command doesn't work. Often times, The class cannot be instantiated with the client as an argument.
```py
async def setup(client):
    classes = getmembers(modules[__name__], isclass)
    main_class = classes[0][1]
    await client.add_cog(main_class(client))
```