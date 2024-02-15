import discord
from discord.ext import commands
from source.bot.utils import BaseEmbed, CogAlert
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
import asyncio as IO
import httpx, aiohttp

class Ship(commands.Cog): #I FEEL ILL BADD FOR MAKING THIS COMMAND AHDHHDSHFHSDFSDFSDFSDFGDFGDFGRET
    def __init__(self, client):
        self.client = client

    def name_compatibility(self, name1, name2):
        # Convert both names to lowercase and remove any spaces or punctuation
        name1 = name1.lower().replace(" ", "").replace(".", "").replace(",", "")
        name2 = name2.lower().replace(" ", "").replace(".", "").replace(",", "")

        # Assign a numerical value to each letter of the alphabet
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        values = {letter: i + 1 for i, letter in enumerate(alphabet)}

        # For each name, calculate the sum of the numerical values of its letters, vowels, consonants, and syllables
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        name1_letters = sum(values[letter] for letter in name1)
        name1_vowels = sum(values[letter] for letter in name1 if letter in vowels)
        name1_consonants = sum(values[letter] for letter in name1 if letter in consonants)
        name1_syllables = len(name1) // 3 + 1 # A simple way to estimate the number of syllables
        name2_letters = sum(values[letter] for letter in name2)
        name2_vowels = sum(values[letter] for letter in name2 if letter in vowels)
        name2_consonants = sum(values[letter] for letter in name2 if letter in consonants)
        name2_syllables = len(name2) // 3 + 1 # A simple way to estimate the number of syllables

        # Compare the results of both names and find the difference between them for each parameter
        diff_letters = abs(name1_letters - name2_letters)
        diff_vowels = abs(name1_vowels - name2_vowels)
        diff_consonants = abs(name1_consonants - name2_consonants)
        diff_syllables = abs(name1_syllables - name2_syllables)

        # Divide the difference by the maximum possible value for each parameter and multiply by 100 to get a percentage
        max_letters = 26 * 10 # Assuming the longest name has 10 letters
        max_vowels = 5 * 10 # Assuming the longest name has 10 vowels
        max_consonants = 21 * 10 # Assuming the longest name has 10 consonants
        max_syllables = 4 * 10 # Assuming the longest name has 10 syllables
        perc_letters = diff_letters / max_letters * 100
        perc_vowels = diff_vowels / max_vowels * 100
        perc_consonants = diff_consonants / max_consonants * 100
        perc_syllables = diff_syllables / max_syllables * 100

        # Subtract the percentage from 100 to get the compatibility score for each parameter
        score_letters = 100 - perc_letters
        score_vowels = 100 - perc_vowels
        score_consonants = 100 - perc_consonants
        score_syllables = 100 - perc_syllables

        # Average the compatibility scores for all parameters to get the final compatibility score
        final_score = (score_letters + score_vowels + score_consonants + score_syllables) / 4

        # Return the final compatibility score
        return final_score
    # TODO: Add a condition, and a different effect, suppose that the name_compatibility is lower than 50%, we can put
    # TODO: broken heart, and so, if name_compatibility is lower than 0%, we change background image to graveyard
    # TODO: and so if it is 100% put mini hearts above the head.
    async def create_image_merger(self, name1, name2):
        async with aiohttp.ClientSession() as session:
            async def load_image(url):
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)
                    if response.status_code != 200:
                        return "Err non-200"
                    return BytesIO(response.content)

            REQ_PFP_1, REQ_PFP_2, background, love_icon, heart, heart2 = await IO.gather(
                load_image(str(name1.display_avatar)),
                load_image(str(name2.display_avatar)),
                load_image('https://img.freepik.com/free-vector/set-torii-gates-water_52683-44986.jpg'),
                load_image('https://purepng.com/public/uploads/large/heart-icon-jst.png'),
                load_image('https://i.pinimg.com/originals/bf/c5/14/bfc51405ddf0003dd91dce19325a22ef.png'),
                load_image('https://www.vhv.rs/dpng/f/133-1337618_red-sparkles-png.png'),
            )
        img_1 = Image.open(REQ_PFP_1)
        img_2 = Image.open(REQ_PFP_2)
        img_1 = img_1.resize((170, 170))
        img_2 = img_2.resize((170, 170))
        img_1.save("image.png")
        img_2.save("image.png")
        # create a mask for the circle shape
        mask = Image.new("L", (170, 170), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 170, 170), fill=255)
        # apply the mask to both images
        img_1 = ImageOps.fit(img_1, mask.size, centering=(0.5, 0.5))
        img_1.putalpha(mask)
        img_2 = ImageOps.fit(img_2, mask.size, centering=(0.5, 0.5))
        img_2.putalpha(mask)
        # create a new canvas with transparent background
        canvas = Image.new("RGBA", (400, 230), (0, 0, 0, 0))
        # paste the images in the center of the canvas
        
        bg_img = Image.open(background)
        bg_img = bg_img.resize((400, 230))
        # paste the background image onto the canvas
        canvas.paste(bg_img)
        
        canvas.paste(img_1, (40, 28), img_1)
        canvas.paste(img_2, (185, 28), img_2)
        # load and resize the love icon
        love_img = Image.open(love_icon)
        love_img = love_img.resize((90, 90))
        love_img = love_img.convert (canvas.mode)
        # paste the love icon between the two pictures
        canvas.paste(love_img, (155, 62), love_img)
        
        heart = Image.open(heart)
        heart = heart.resize((130, 130))
        heart = heart.convert (canvas.mode)
        canvas.paste(heart, (50, -10), heart)
        
        heart2 = Image.open(heart2)
        heart2 = heart2.resize((130, 60))
        heart2 = heart2.convert (canvas.mode)
        canvas.paste(heart2, (200, 10), heart2)
        return canvas

    @commands.command()
    async def ship(self, ctx, user_1, user_2):
        user_1_p = await self.client.fetch_user(int(user_1[2:-1]))
        user_2_p = await self.client.fetch_user(int(user_2[2:-1]))
        if user_1_p is None or user_2_p is None:
            await BaseEmbed(ctx, "Invalid user IDs", Color=(255, 0, 0))
            return
        CogAlert(ctx.author.name)
        # Call the pfps merger lmao, why i kept laughing at this command lmdsfsdf
        canvas = await self.create_image_merger(user_1_p, user_2_p)

        # Save .png in Memory
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        buffer.seek(0)

        # Create discord file from the Image.
        File = discord.File(buffer, filename="canvas.png")
        user_1, user_2 = await self.client.fetch_user(int(user_1[2:-1])), await self.client.fetch_user(int(user_2[2:-1]))
        compatibility = self.name_compatibility(str(user_1), str(user_2))
        await ctx.channel.send('## :heart_on_fire: :heart_on_fire: :heart_on_fire: **MATCHMAKING** :heart_on_fire: :heart_on_fire: :heart_on_fire:', embed=discord.Embed(
            title=f"**{user_1}** X **{user_2}**",
            description=f'**{user_1}** compatibility with **{user_2}** is! ||**{str(round(compatibility, 2))}**||%',
            color=discord.Color.pink(),
        ), file=File)
        

async def setup(client):
    await client.add_cog(Ship(client))