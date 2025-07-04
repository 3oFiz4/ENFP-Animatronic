# ENFP-Animatronic (abandoned) 🤖
Welcome to my very first Github project I work with someone!

Yo, what's good? Welcome to the home of the most chaotic, fun-loving Discord bot out there, designed exclusively for our squad of ENFPs. 🎉

This bot is all about bringing the party to our server with minigames, surprises, and a whole lot more. It's like having a virtual party animal right in your chat! 🎮🎈


Stay tuned, it's about to get lit! 🔥"!
## 🌈 What's Inside?
- **cogs/note** This is a list of command for adding a note.
- **cogs/birthday** This is a list of command for handling and tracking a birthday.
- **cogs/misc** This is a list of command for handling and tracking a birthday.
- **cogs/matching** This is a list of command for matching user with another user command.
- **cogs/debate** This is a list of command for dealing with a One-Turn-Based debate.
<details>
  <summary>Command list:</summary>
  
  ```python
    # WE ARE ASSUMING, WE ARE USING ";" AS THE COMMAND'S PREFIX
    # * means optional

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
    >clear [NUMBER_OF_MESSAGES:int] ## Delete [NUMBER_OF_MESSAGES] above.
    >clear_until [MESSAGE:ID] ## Delete every messages, until a message with the same message_ID are found, it will stop deleting (EXCLUSIVE).
    >log_until [MESSAGE:ID] [TUPLE_LIKE_STRING]
    ## The parameter in TUPLE_LIKE_IN_STRING are below:
    ## (1st param) show_author = 1
    ## (2nd param) show_author_id = 1
    ## (3rd param) show_msg = 1
    ## (4th param) show_msg_id = 1
    ## (5th param) show_msg_created_at = 1
    ## e.g. `;log_until "1207784045661130819" "(1, 0, 1, 0, 0)" `

    # Matching related commands:
    ## discord.User is a datatype, which you can trigger using @[USERNAME]
    >ship [FIRST_USER:discord.User] [SECOND_USER:discord.User]
    ## e.g. `;ship @Nakiwa @Cleo`
    >zamn [USER:discord.User] ## Put your profile in a zamn template.... lmfao.

    # AI Related commands:
    >askenfp [TEXT:str] ## It simply give the GPT a text, which will be output to current channel.
    ## e.g. `;askenfp Why US's human rights is collapsed`

    # Debate related commands:
    >helpdebate ## Explain how to use the command. I suggest run this command first, before playing with the commands.
    >topic [TOPIC:str] ## Start a debate regarding the topic.
    # e.g. `;topic Why US's human rights is collapsed`
    >join ## Join a debate, if only the debate is unsealed.
    >pass ## Let next participant have a speak, after yours.
    >seal ## Seal the debate, so no one can join.
    >unseal ## Unseal the debate, so anyone can join. You'll use this after you `>seal` the debate. 
    >end ## End the debate.

    # Truth or Dare commands:
    >dare *[ID:int] ## Retrieve a randomized or a selected ID of a dare from the DB
    >truth *[ID:int] ## Retrieve a randomized or a selected ID of a truth from the DB
    >request [TYPE:Dare | Truth] [TEXT:str] ## Upload a Dare or Truth content to the DB
    ## e.g. `;request Dare lick a soap`
```
    We will add more commands in the future. THis project is still far far far away from complete! So please be patient!
</details>

<details>
  <summary>Database table</summary>

  **Incase you are wondering, how the database table should looks like. It should look like this:**
  ![](./assets/dbname.png)

  **Each table should looks like this:**
  1. **TABLE/TOD** (Handling Truth or Dare):
  ![](./assets/dbtod.png)
  2. **TABLE/birthdays** (Handling birthdays):
  ![](./assets/dbbday.png)
  3. **TABLE/notes** (Handling notes):
  ![](./assets/dbnotes.png)
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
```py
# Remove any comment that start with hashtags!

PROJECT_ROOT="YOUR_PROJECT_ABSOLUTE_PATH"
YOUR_BOT_ACCOUNT_TOKEN="YOUR_BOT_TOKEN"
SUPABASE_URL="YOUR_SUPABASE_URL"
SUPABASE_KEY="YOUR_SUPABASE_KEY"
AI_API_KEY="YOUR_API_KEY" # Optional, but you cannot run `>askenfp`
AI_API_BASE="YOUR_API_ENDPOINT" # Optional, but you cannot run `>askenfp`
AI_MODEL="YOUR_AI_MODEL" # Optional, but you cannot run `>askenfp`
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
