# ENFP-Animatronic (UNFINISHED) 🤖
Yo, what's good? Welcome to the home of the most chaotic, fun-loving Discord bot out there, designed exclusively for our squad of ENFPs. 🎉

This bot is all about bringing the party to our server with minigames, surprises, and a whole lot more. It's like having a virtual party animal right in your chat! 🎮🎈


Stay tuned, it's about to get lit! 🔥"!
## UPDATE TODO
![image](https://github.com/DaemonPooling/ENFP-Animatronic/assets/157283533/5467b4a5-58e7-4108-ba38-e9333ef93a72)
## 🌈 What's Inside?
- **cogs/note** This is a list of command for adding a note.
- **cogs/birthday** This is a list of command for handling and tracking a birthday.
- **cogs/misc** This is a list of command for handling and tracking a birthday.
- **cogs/matching** This is a list of command for matching user with another user command.
<details>
  <summary>Command list:</summary>
  
  ```python
    # WE ARE ASSUMING, WE ARE USING ";" AS THE COMMAND'S PREFIX

    # Notes related commands:
    >addnote [TEXT:str] ## Add a note 
    >editnote [NOTE_ID:int] [TEXT:str] ## Edit a specific note id's content
    >listnote ## List your note
    >removenote [NOTE_ID:int] ## Remove a specific note id

    # Birthday related commands:
    >showbirthday [USER_ID:int] ## Show anyone's birthday
    ## e.g. `>showbirthday 901404605336916018`
    >setbirthday [DATE: Format(%d-%m)] ## Set your birthday
    ## e.g. `>setbirthday 03-03` will give 3 March
    >listbirthday ## List everyone birthday in order
    >forgetbirthday ## Remove your birthday from the D

    # Misc related commands:
    >sing [ARTIST:str] [MUSIC_NAME:str] [DELAY:int] [SING_TOGETHER: 1 | 0] ## Sing a specific song with/without a bot.
    >texttosha256 [TEXT:str] ## Encrypt text to SHA256

    # Matching related commands:
    ## discord.User is a datatype, which you can trigger using @[USERNAME]
    >ship [FIRST_USER:discord.User] [SECOND_USER:discord.User]
    ## e.g. `>ship @Nakiwa @Cleo`
```
    We will add more commands in the future. THis project is still far far far away from complete! So please be patient!
</details>



## 📜 Instructions:
1. **Clone the repository:**
```bash
git clone https://github.com/DaemonPooling/ENFP-Animatronic
```

2. **Navigate to the Project Folder:**
```bash
cd ENFP-Animatronic
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create and configure the environment variables (.env): (I assume you know how to do this)**
```
PROJECT_ROOT="YOUR_PROJECT_ABSOLUTE_PATH"
YOUR_BOT_ACCOUNT_TOKEN="YOUR_BOT_TOKEN"
SUPABASE_URL="YOUR_SUPABASE_URL"
SUPABASE_KEY="YOUR_SUPABASE_KEY"
```

5. **You can modify the script configuration aswell! on (source/config.json)** 

6. **Locate through source directory:**
```bash
cd source/bot
```

7. **Run bot.py:**
```bash
python bot.py
```