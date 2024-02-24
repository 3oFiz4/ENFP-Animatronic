import discord
from discord.ext import commands
from source.bot.utils import BaseEmbed, CogAlert
from PIL import Image, ImageDraw, ImageOps, ImageFont
from io import BytesIO
import asyncio as IO
import httpx, aiohttp
import json
import os
from urllib.parse import urlparse

with open("../config.json") as f:config = json.load(f)

class QuoteMaker(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def create_image_merger(self, name1):
        async with aiohttp.ClientSession() as session, httpx.AsyncClient() as client:
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
                load_image('./background_asset/grad.png')
            )
            img_1 = Image.open(REQ_PFP_1)
            img_1 = img_1.resize((300, 300))
            img_1.save("image.png")
            # create a mask for the circle shape
            mask = Image.new("L", (300, 300), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 300, 300), fill=255)
            img_1 = ImageOps.fit(img_1, mask.size, centering=(0.5, 0.5))
            img_1.putalpha(mask)

            img = Image.new("RGB", (400, 230), (0, 0, 0, 0))

            # TODO: Find a way to insert a font, as for now, the text is "Fukuma Mizushi.", it should be placed right in the center of the canvas.
            
            # create a font
            font = ImageFont.truetype("arial.ttf", 20)

            # create a drawing context
            draw = ImageDraw.Draw(img)

            # create a textbox
            textbox = (50, 50, 350, 180)

            # draw a rectangle around the textbox
            draw.rectangle(textbox, outline="white")

            # draw text in the textbox
            text = "This is a textbox that can resize and position itself automatically."
            draw.text(textbox, text, font=font, fill="white", anchor="mm", align="center")

            # save the image
            img.save("textbox.png")        
            
            # create a new canvas with transparent background
            canvas = Image.new("RGBA", (400, 230), (0, 0, 0, 0))

            # paste the profile picture onto the canvas
            canvas.paste(img_1, (-50, -35), img_1)

            # paste the background image onto the canvas
            bg_img = Image.open(background)
            bg_img = bg_img.resize((400, 230))
            canvas.paste(bg_img, mask=bg_img)
            
            return canvas

    @commands.command()
    async def quotemaker(self, ctx, user_1):
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
        await ctx.channel.send(file=File)
        

async def setup(client):
    await client.add_cog(QuoteMaker(client))