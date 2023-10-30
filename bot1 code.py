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

bot = commands.Bot(command_prefix = "!", intents = intents)


@bot.event
async def on_ready():
    print("Bot is running...")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)



@bot.command(name = "hello")
async def greeting(ctx):
    username = str(ctx.author).split('#')[0]
    await ctx.channel.send(f"Greetings {username}!")

@bot.command()
async def print(ctx, *args):
    response = ""
    if len(args):
        for arg in args:
            response = response + " " + arg
        await ctx.channel.send(response)
    return
	
@bot.tree.command(name="hello")
async def hello(interaction:discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!", ephemeral=True)

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction:discord.Interaction, thing_to_say:str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

bot.run(os.environ.get('TOKEN'))
