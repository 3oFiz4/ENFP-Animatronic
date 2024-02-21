import discord
from discord.ext import commands
from source.bot.utils import BaseEmbed, CogAlert
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
import asyncio as IO
import httpx, aiohttp
import random
import json
import sys
import os
from urllib.parse import urlparse

with open("../config.json") as f:config = json.load(f)

class Zamn(commands.Cog): #I FEEL ILL BADD FOR MAKING THIS COMMAND AHDHHDSHFHSDFSDFSDFSDFGDFGDFGRET
    def __init__(self, client):
        self.client = client
    
    async def create_image_merger(self, name1):
        async with aiohttp.ClientSession() as session, httpx.AsyncClient() as client:
            #? What this function does is to retrieve a given URL, and then downloading it (The reason we did this, because we are assuming that the user might trigger the same command, and for the sake of performance), after that, assuming the user trigger this command again, instead it will check if the URL given are equal to any file in `background_asset/`, if it found one, it will re-use that one instead, and if it doesn't found one, it will repeat the first process, which is to retrieve a given URL
            async def load_image(url):
                parsed_url = urlparse(url)
                image_name = os.path.basename(parsed_url.path)
                dir_path = os.path.dirname(os.path.realpath(__file__))
                local_path = os.path.join(dir_path, 'background_asset', image_name)

                if os.path.exists(local_path):
                    with open(local_path, 'rb') as f:
                        return BytesIO(f.read())
            async def load_profile(url):
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)
                    if response.status_code != 200:
                        return "Err non-200"
                    return BytesIO(response.content)
            REQ_PFP_1, background = await IO.gather(
                load_profile(str(name1.display_avatar)),
                load_image('./background_asset/zamn.png')
            )
            img_1 = Image.open(REQ_PFP_1)
            img_1 = img_1.resize((195, 195))
            img_1.save("image.png")
            # create a mask for the circle shape
            mask = Image.new("L", (170, 170), 0)
            draw = ImageDraw.Draw(mask)
            # create a new canvas with transparent background
            canvas = Image.new("RGBA", (400, 230), (0, 0, 0, 0))
            # paste the images in the center of the canvas
            bg_img = Image.open(background)
            bg_img = bg_img.resize((400, 230))
            # paste the background image onto the canvas
            canvas.paste(bg_img)
            
            canvas.paste(img_1, (200, 33), img_1)
            # load and resize the love icon
            
            return canvas

    @commands.command()
    async def zamn(self, ctx, user_1):
        user_1_p = await self.client.fetch_user(int(user_1[2:-1]))
        if user_1_p is None:
            await BaseEmbed(ctx, "Invalid user IDs", Color=(255, 0, 0))
            return
        CogAlert(ctx.author.name)
        canvas = await self.create_image_merger(user_1_p)

        # Save .png in Memory
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        buffer.seek(0)
 
        # Create discord file from the Image.
        File = discord.File(buffer, filename="canvas.png")
        user_1 = await self.client.fetch_user(int(user_1[2:-1]))
        await ctx.channel.send('# ZAMN!', file=File)
        

async def setup(client):
    await client.add_cog(Zamn(client))