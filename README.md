# ENFP-Animatronic (UNFINISHED) 🤖
Yo, what's good? Welcome to the home of the most chaotic, fun-loving Discord bot out there, designed exclusively for our squad of ENFPs. 🎉

This bot is all about bringing the party to our server with minigames, surprises, and a whole lot more. It's like having a virtual party animal right in your chat! 🎮🎈

Here's what we're cooking up:

- [ ] Prep Time: Getting all our ducks in a row before the real fun begins. 🦆
- [ ] The Big Idea: Brainstorming all the wild things this bot will be able to do. 💡
- [ ] File Structure: Organizing our bot's brain so it can keep up with us. 🗂️
- [ ] Commands: The magic words to make our bot do its thing. 🗣️

Stay tuned, it's about to get lit! 🔥"!

## 🌈 What's Inside?
- **maincog.py:** This is a test command, to see if the Discord cogs working as expected or not.
- **addnote.py** This is a command for adding a note. Such command can be described below.
```bash
>addnote "YOUR_TEXT"

# example
>addnote "This is a note"
```
- **editnote.py** This is a command for edit a note. Such command can be described below.
```bash
>editnote YOUR_NOTE_ID "YOUR_TEXT"

# example
>editnote 6 "The new note"
```
- **listnote.py** This is a command for list a notes. Such command can be described below.
```bash
>listnote

# example
>listnote
```
- **removenote.py** This is a command for remove a note. Such command can be described below.
```bash
>removenote YOUR_NOTE_ID

# example
>removenote 6 # will remove the note with id of 6.
```

We will add more commands in the future. THis project is still far far far away from complete! So please be patient!

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

5. **Locate through source directory:**
```bash
cd source/bot
```

6. **Run bot.py:**
```bash
python bot.py
```