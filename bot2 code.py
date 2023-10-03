# Import the discord.py library
import discord
from discord.ext import commands

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix="!")

# Define a global dictionary to store the user pairs
user_pairs = {}

# Define a command to pair two users
@bot.command()
async def pair(ctx, user1: discord.Member, user2: discord.Member):
    # Check if the users are already paired
    if user1 in user_pairs or user2 in user_pairs:
        await ctx.send("Sorry, one of the users is already paired with someone else.")
    else:
        # Add the users to the dictionary
        user_pairs[user1] = user2
        user_pairs[user2] = user1
        # Send a confirmation message
        await ctx.send(f"Successfully paired {user1.mention} and {user2.mention}.")

# Define a command to unpair two users
@bot.command()
async def unpair(ctx, user: discord.Member):
    # Check if the user is paired
    if user in user_pairs:
        # Get the other user
        other_user = user_pairs[user]
        # Remove the users from the dictionary
        user_pairs.pop(user)
        user_pairs.pop(other_user)
        # Send a confirmation message
        await ctx.send(f"Successfully unpaired {user.mention} and {other_user.mention}.")
    else:
        # Send an error message
        await ctx.send("Sorry, the user is not paired with anyone.")

# Define an event handler for when a message is sent in a channel
@bot.event
async def on_message(message):
    # Check if the message is from a paired user
    if message.author in user_pairs:
        # Get the other user
        other_user = user_pairs[message.author]
        # Check if the message mentions the other user
        if other_user in message.mentions:
            # Send a direct message to the other user with the message content
            await other_user.send(f"{message.author.mention} pinged you: {message.content}")
        else:
            # Send a direct message to the other user with the message content and a ping
            await other_user.send(f"{message.author.mention} sent you a message: {message.content}\n{other_user.mention}")
    # Process the message for commands
    await bot.process_commands(message)

# Run the bot with a token
bot.run("TOKEN")
