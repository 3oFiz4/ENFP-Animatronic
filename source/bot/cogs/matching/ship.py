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
import time
import math
import hashlib
from urllib.parse import urlparse

with open("../config.json") as f:config = json.load(f)

class Ship(commands.Cog): #I FEEL ILL BADD FOR MAKING THIS COMMAND AHDHHDSHFHSDFSDFSDFSDFGDFGDFGRET
    def __init__(self, client):
        self.client = client
    
    def name_compatibility(self, name1, name2):
        def det(a, b): # DETERMINANT RANDOM
            current_time = time.time()  # Get the current time
            frac, _ = math.modf(current_time)  # Get the fractional part of the current time
            return a + int((b - a + 1) * frac)  # Scale the fractional part to the range [a, b]
        
        def Lev_distance(name1, name2):
            matrix = [[0 for j in range(len(name2) + 1)] for i in range(len(name1) + 1)]
            for i in range(len(name1) + 1):
                matrix[i][0] = i
            for j in range(len(name2) + 1):
                matrix[0][j] = j
            for i in range(1, len(name1) + 1):
                for j in range(1, len(name2) + 1):
                    cost = 0 if name1[i - 1] == name2[j - 1] else 1
                    matrix[i][j] = min(matrix[i - 1][j] + 1,
                                    matrix[i][j - 1] + 1,
                                    matrix[i - 1][j - 1] + cost) 
            return matrix[len(name1)][len(name2)]
        
        # Convert both names to lowercase and remove any spaces or punctuation
        name1 = name1.lower().replace(" ", "").replace(".", "").replace(",", "")
        name2 = name2.lower().replace(" ", "").replace(".", "").replace(",", "")

        # Assign a numerical value to each letter of the alphabet
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        values = {letter: i + 1 for i, letter in enumerate(alphabet)}

        # For each name, calculate the sum of the numerical values of its letters, vowels, consonants, and syllables
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        name1_letters = sum(ord(letter) for letter in name1)
        name1_vowels = sum(values[letter] for letter in name1 if letter in vowels)
        name1_consonants = sum(values[letter] for letter in name1 if letter in consonants)
        name1_syllables = len(name1) // 3 + 1 # A simple way to estimate the number of syllables
        name2_letters = sum(ord(letter) for letter in name2)
        name2_vowels = sum(values[letter] for letter in name2 if letter in vowels)
        name2_consonants = sum(values[letter] for letter in name2 if letter in consonants)
        name2_syllables = len(name2) // 3 + 1 # A simple way to estimate the number of syllables

        # Compare the results of both names and find the difference between them for each parameter
        diff_letters = abs(name1_letters - name2_letters)
        diff_vowels = abs(name1_vowels - name2_vowels)
        diff_consonants = abs(name1_consonants - name2_consonants)
        diff_syllables = abs(name1_syllables - name2_syllables)

        # Divide the difference by the maximum possible value for each parameter and multiply by 100 to get a percentage
        max_letters = 26 * 30 # Assuming the longest name has 30 letters
        max_vowels = 5 * 30 # Assuming the longest name has 30 vowels
        max_consonants = 21 * 30 # Assuming the longest name has 30 consonants
        max_syllables = 4 * 30 # Assuming the longest name has 30 syllables
        perc_letters = diff_letters / max_letters * 100
        perc_vowels = diff_vowels / max_vowels * 100
        perc_consonants = diff_consonants / max_consonants * 100
        perc_syllables = diff_syllables / max_syllables * 100

        # Subtract the percentage from 100 to get the compatibility score for each parameter
        score_letters = 100 - perc_letters
        score_vowels = 100 - perc_vowels
        score_consonants = 100 - perc_consonants
        score_syllables = 100 - perc_syllables
        Lev = Lev_distance(name1, name2)
        Lev_normalized = Lev / max(len(name1), len(name2)) * 100
        # Average the compatibility scores for all parameters to get the final compatibility score
        final_score = (det(score_letters, perc_letters) + det(score_vowels, perc_vowels) + det(score_consonants, perc_consonants) + det(score_syllables, perc_syllables) + det(Lev_normalized, Lev)) / 5
        name_sim = 100 - Lev_normalized
        return det(det(final_score, name_sim), 100)
    # TODO: Rather than actually download each link in an Image, and for the sake of time complexity. User will be prompted to download the images, then store in an assets, and then load the Image. Which benefit a large speeds.
    async def create_image_merger(self, name1, name2, percentage):
        Possible_background = config['SHIP']['POSSIBLE_BACKGROUND']
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
                else:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url)
                        if response.status_code != 200:
                            return "Err non-200"
                        with open(local_path, 'wb') as f:
                            f.write(response.content)
                        with open(local_path, 'rb') as f:
                            return BytesIO(f.read())
            #? Similar to above function, but instead this one doesn't downloading the given URL. And only download it (everytime user trigger this command)
            async def load_profile(url):
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)
                    if response.status_code != 200:
                        return "Err non-200"
                    return BytesIO(response.content)
            # If Percentage is 100%-80%
            if percentage >= 80:
                REQ_PFP_1, REQ_PFP_2, background, love_icon, heart, heart2 = await IO.gather(
                    load_profile(str(name1.display_avatar)),
                    load_profile(str(name2.display_avatar)),
                    load_image(random.choice(Possible_background)),
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
            # If Percentage is 80%-50%
            elif percentage >= 50:
                REQ_PFP_1, REQ_PFP_2, background, love_icon = await IO.gather(
                    load_profile(str(name1.display_avatar)),
                    load_profile(str(name2.display_avatar)),
                    load_image(random.choice(Possible_background)),
                    load_image('https://purepng.com/public/uploads/large/heart-icon-jst.png'),
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
                return canvas
            # If Percentage is 50%-20%
            elif percentage >= 20:
                REQ_PFP_1, REQ_PFP_2, background, love_icon = await IO.gather(
                    load_profile(str(name1.display_avatar)),
                    load_profile(str(name2.display_avatar)),
                    load_image('https://img.freepik.com/free-photo/beautiful-shot-tall-trees-forest-fog-surrounded-by-plants_181624-2352.jpg'),
                    load_image('https://pngimg.com/uploads/broken_heart/broken_heart_PNG39.png'),
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
                return canvas
            # If Percentage is 20%-0% literally unloved.
            elif percentage >= 0:
                REQ_PFP_1, background = await IO.gather(
                    load_profile(str(name1.display_avatar)),
                    load_image('https://img.freepik.com/free-vector/halloween-background-with-old-cemetery-gravestones-spooky-leafless-trees-full-moon-night-sky-realistic-illustration_1284-65419.jpg'),
                )
                img_1 = Image.open(REQ_PFP_1)
                img_1 = img_1.resize((170, 170))
                img_1.save("image.png")
                # create a mask for the circle shape
                mask = Image.new("L", (170, 170), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 170, 170), fill=255)
                # apply the mask to both images
                img_1 = ImageOps.fit(img_1, mask.size, centering=(0.5, 0.5))
                img_1.putalpha(mask)
                # create a new canvas with transparent background
                canvas = Image.new("RGBA", (400, 230), (0, 0, 0, 0))
                # paste the images in the center of the canvas
                
                bg_img = Image.open(background)
                bg_img = bg_img.resize((400, 230))
                # paste the background image onto the canvas
                canvas.paste(bg_img)
                canvas.paste(img_1, (120, 28), img_1)
                return canvas

    @commands.command()
    async def ship(self, ctx, user_1, user_2):
        user_1_p = await self.client.fetch_user(int(user_1[2:-1]))
        user_2_p = await self.client.fetch_user(int(user_2[2:-1]))
        if user_1_p is None or user_2_p is None:
            await BaseEmbed(ctx, "Invalid user IDs", Color=(255, 0, 0))
            return
        CogAlert(ctx.author.name)
        compatibility = self.name_compatibility(str(user_1), str(user_2))
        # Call the pfps merger lmao, why i kept laughing at this command lmdsfsdf
        canvas = await self.create_image_merger(user_1_p, user_2_p, compatibility)

        # Save .png in Memory
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        buffer.seek(0)

        def reply(percentage):
            if percentage >= 80:
                return random.choice([
                    "You really got soulmate, heh! :wink:",
                    "Congrats! You found the one! :heart_on_fire:",
                    "Seems you hit the jackpot! ^_^!",
                    "WOW! You just struck a jackpot! :coin:",
                    "You just scored a goal! :soccer:",
                    "You and your match are blash! :boom:",
                    "You just landed a moonshot! :rocket:",
                    "Sweet treat baby! :lollipop:",
                    "You got rizz."
                ])
            elif percentage >= 50:
                return random.choice([
                    "Wow! You got someone to crush on, maybe :grin:?",
                    "Sheshhh, congrats!",
                    "Your family arc starting now :wink:",
                    "Luck+++",
                    "WOWOWOWO!!111! :flushed:",
                    ":eyes:*bombastic sideeyes*:eyes:",
                ]),
            elif percentage >= 20:
                return random.choice([
                    "Hey.. Sorry to hear that! I know there are many great people that loves you!",
                    "Awhh, it's fine my friend! The developer of this bot love you though!",
                    "It's fine. You could try again to seek for Love, right :wink:",
                    "Come on man. Don't give up! Try to match with other people!",
                    "It's fine... *pat shoulder*",
                    ":people_hugging: sorry man...",
                ]),
            elif percentage >= 0:
                return random.choice([
                    "... Hey it's lonely here, should we match with other one?",
                    "Let's try with another match :)",
                ]),
            
        # Create discord file from the Image.
        File = discord.File(buffer, filename="canvas.png")
        user_1, user_2 = await self.client.fetch_user(int(user_1[2:-1])), await self.client.fetch_user(int(user_2[2:-1]))
        await ctx.channel.send('## :heart_on_fire: :heart_on_fire: :heart_on_fire: **MATCHMAKING** :heart_on_fire: :heart_on_fire: :heart_on_fire:', embed=discord.Embed(
            title=f"**{user_1}** X **{user_2}**",
            description=f'**{user_1}** compatibility with **{user_2}** is! ||**{str(round(compatibility, 2))}**||%\n{reply(compatibility)}',
            color=discord.Color.pink(),
        ), file=File)
        

async def setup(client):
    await client.add_cog(Ship(client))