import discord
from discord.ext import commands

class LogMessages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def log_until(self, ctx, message_id, formats='(1, 1, 1, 1, 1)'):
        formats = formats.strip('()')
        formats = formats.split(',') 
        formats = tuple(bool(int(x)) for x in formats)
        channel = ctx.channel
        msg = await channel.fetch_message(message_id)
        msgs = [msg async for msg in channel.history(after=msg, limit=200, oldest_first=False)]
        file_name = f"{channel.id}_LOG.log" 
        file = open(file_name, "w") 
        for message in msgs:
            au = message.author.name if formats[0] else ''
            au_id = f' ({message.author.id})' if formats[1] else ''
            msg = f'|"""{message.content}"""|' if formats[2] else ''
            msg_id = f' ({message.id})' if formats[3] else ''
            msg_created = f' <{message.created_at}>' if formats[4] else ''  
            file.write(f'{au}{au_id}\t:::\t{msg}{msg_id}{msg_created}\n')
        file.close() # close the file
        await ctx.author.send(file=discord.File(file_name)) # send the file to the person who triggered the command

async def setup(client):
    await client.add_cog(LogMessages(client))
