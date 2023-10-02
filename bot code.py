# Imports
import os 
import discord
import aiohttp

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True


### ---------- discord.Client ---------- ### 
# Represents a client connection that connects to Discord. 
# This class is used to interact with the Discord WebSocket and API.

# client = discord.Client(intents = intents)

### ---------- commands.Bot ---------- ### 
# Represents a Discord bot. 
# This is a sub class of 'discord.Client' and as a result 
# anything you can do with 'discord.Client' you can do with this bot.

bot = commands.Bot(command_prefix = "$", intents = intents)


# On start up
@bot.event
async def on_ready():
    print("Bot is running...")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)


### ---------- ($) commands ---------- ### 

# Greeting
@bot.command(name = "hello")
async def greeting(ctx):
    username = str(ctx.author).split('#')[0]
    await ctx.channel.send(f"Greetings {username}!")

# Print test
@bot.command()
async def print(ctx, *args):
    response = ""
    if len(args):
        for arg in args:
            response = response + " " + arg
        await ctx.channel.send(response)
    return

# API request test
@bot.command(name = "dog")
async def dog_image(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://dog.ceo/api/breeds/image/random") as r:
            data = await r.json()
            embed = discord.Embed(title = "Woof")
            embed.set_image(url = data['message'])
            await ctx.send(embed = embed)


### ---------- Forward slash commands ---------- ### 

# Returns a greeting along with a tagged/mentioned username of the user
@bot.tree.command(name="hello")
async def hello(interaction:discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!", ephemeral=True)

# The bot posts whatever the user passes through as an argument
@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction:discord.Interaction, thing_to_say:str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

# Grabs a random image of a dog
@bot.tree.command(name="dog")
async def dog(interaction: discord.Interaction):
    url = "https://dog.ceo/api/breeds/image/random"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            data = await r.json()
            embed = discord.Embed(title = "Woof")
            embed.set_image(url = data['message'])
            await interaction.response.send_message(embed = embed)

# Passes keywords as a parameter to search through the steam API and returns the first game found.
@bot.tree.command(name="steam_search")
@app_commands.describe(key_word = "What to search?")
async def steam_search(interaction:discord.Interaction, key_word:str):
    url = f"https://steam2.p.rapidapi.com/search/{key_word}/page/1"
    headers = {
	"X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
	"X-RapidAPI-Host": "steam2.p.rapidapi.com"
    }
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, headers = headers) as r:
                data = await r.json()
                await interaction.response.send_message(str(data[0]['url']))
    except Exception as e:
        await interaction.response.send_message(f"Unable to find `{key_word}`.", ephemeral=True)

# Translator API
@bot.tree.command(name="translate_text")
@app_commands.describe(language = "Which language?", source_text = "What would you like translated?")
async def translate_text(interaction:discord.Interaction, language:str, source_text:str):
    url = "https://text-translator2.p.rapidapi.com/translate"
    payload = f"source_language=en&target_language={language}&text={source_text}"
    headers = {
    "content-type": "application/x-www-form-urlencoded",
	"X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
	"X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
    }
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, data = payload, headers = headers) as r:
                data = await r.json()
                await interaction.response.send_message(f"{data['data']['translatedText']}")
    except Exception as e:
        await interaction.response.send_message("Failed attempt", ephemeral=True)



# Run the bot
bot.run(os.environ.get('TOKEN'))
