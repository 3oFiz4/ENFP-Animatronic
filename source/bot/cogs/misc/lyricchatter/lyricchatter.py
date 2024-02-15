
# === MODULE SECTION === #
import discord
from discord.ext import commands
from source.bot.utils import BaseEmbed, CogAlert
import re # Regexp
from bs4 import BeautifulSoup # Handling the Input and Output of the website and script.
import httpx # Handling request
import asyncio as io # Asynchronous operation
# === MODULE SECTION === #

#! This whole code are copied from https://github.com/DaemonPooling/Discord-lyric-chatter-bot
#! Which is also my own repository

matchURL = "https://genius.com/{Artist}-{Title}-lyrics" # This is a regexp pattern.
stop_singing = False

class LyricChatter(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    async def GET_SONG_LYRIC(self, ctx, Artist, Title):
        # Convert to equivalent URL match. In this case,
        # the Artist param only expect a capitalized letter and the whitespace replaced by '-'
        # the Title param only expect a lowercase letter and the whitespace replaced by '-'
        Artist = Artist.replace(' ', '-').capitalize()
        Title = Title.replace(' ', '-').lower()
        
        # Substitue the Artist and Title variable to the {Artist} and {Title}
        url = matchURL.format(Artist=Artist, Title=Title)

        try:
            async with httpx.AsyncClient() as client:
                # GET req to the URL
                response = await client.get(url)

                # If it is successful (the GET req), then we can continue the script
                if response.status_code == 200:
                    # Return the webpage content as a whole.
                    Body = response.text
                    soup = BeautifulSoup(Body, 'html.parser') 
                    lyric_div = soup.find(class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL') # The lyric container
                    each_lyric = lyric_div.get_text() # Get all content inside the lyric container
                    
                    #TODO: Improvise this regexp part, so it's more efficient.
                    #! Okay, this regexp part might be confusing. So let me tell what each line really does!
                    
                    #? This regexp pattern removes every word that is inside a []. Example, [Intro], [Chorus]
                    each_lyric = re.sub(r'\[.*?\]', '', each_lyric)
                    
                    #? This regexp pattern makes every word that is inside a () into a lowercase word. Example, (Go) becomes (go)
                    #? The reason why I did this, is because the next regexp pattern actually broke the lyric order.
                    each_lyric = re.sub(r'\((.*?)\)', lambda x: x.group().lower(), each_lyric)
                    
                    #? This regexp pattern split the string only when an uppercase letter is followed by a lowercase letter
                    each_lyric = re.split('(?=[A-Z])', each_lyric)
                    
                    #? Final touching, this one simply remove the first element that contains nothing
                    each_lyric = each_lyric[1:len(each_lyric)]
                    return each_lyric
                    
                    # Below code for testing.
                    # for n, i in enumerate(each_lyric):
                    #     print('[',n+1,']', i)
                else:
                    # Else, we send a failed status code.
                    await BaseEmbed(ctx, Title=f"Error: {response.status_code}", Desc=f"Failed, status code: {response.status_code}\nDid you type a proper artist and song? Some music may doesn't exist!", Color=(255, 0, 0))
        except Exception as e:
            # If there's an error occured, please report it to the git issue.
            print(f"Error: {e}")

    @commands.command()
    async def sing(self, ctx, artist: str, title: str, delay: int, together: str='1'):
        await ctx.channel.send(f'**Music name:** {title}\n**By:** {artist}\n**Sing together: {together}**\n**Timeout (delay): {delay}')
        await ctx.message.delete()  # Delete the user's message
        CogAlert(ctx.author.name)
        # Act as a toggler.
        global stop_singing
        stop_singing = False
        # Get the song's lyrics
        song = await self.GET_SONG_LYRIC(ctx, artist, title)

        if (together == '1'):
            for i in range(0, len(song), 2):  # Skip lyric by jumping each element by 2. Example, a,c,e,g instead of a,b,c,d,e,f,g
                if stop_singing:
                    break
                await ctx.send(song[i])  # Bot sings
                try:
                    # Wait for the user's message for up to 'delay' seconds
                    msg = await self.client.wait_for('message', timeout=delay)
                except io.TimeoutError:
                    # If the user doesn't respond in time, stop the lyric from continuing.
                    await BaseEmbed(ctx, 'Info', '**No lyric continuation retrieved. Shutting down lyric\'s continuation**', Color=(255, 255, 0))
                    break
                
        elif (together == '0'):
            # Loop through each lyric
            for lyric in song:
                # Chat the lyric
                await ctx.send(lyric)

                # Delay
                await io.sleep(delay)
        else:
            await BaseEmbed(ctx, Title="Confirmation", Desc='''**Are you sure you type the correct command?**
    Command: >sing [ARTIST:str] [MUSIC_NAME:str] [DELAY:int] [SING_TOGETHER: 1 | 0] ''')

    @commands.command()
    async def stop(self, ctx):
        await BaseEmbed(ctx, 'Music stopped', Color=(255,0,0))
        CogAlert(ctx.author.name)
        global stop_singing
        stop_singing = True
    
async def setup(client):
    await client.add_cog(LyricChatter(client))