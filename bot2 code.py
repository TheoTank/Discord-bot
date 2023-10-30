import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

user_pairs = {}
 users
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

@bot.command()
async def unpair(ctx, user: discord.Member):
    if user in user_pairs:
        other_user = user_pairs[user]
        user_pairs.pop(user)
        user_pairs.pop(other_user)
        await ctx.send(f"Successfully unpaired {user.mention} and {other_user.mention}.")
    else:
        await ctx.send("Sorry, the user is not paired with anyone.")

@bot.event
async def on_message(message):
    if message.author in user_pairs:
        other_user = user_pairs[message.author]
        if other_user in message.mentions:
            await other_user.send(f"{message.author.mention} pinged you: {message.content}")
        else:
            await other_user.send(f"{message.author.mention} sent you a message: {message.content}\n{other_user.mention}")
    await bot.process_commands(message)

bot.run("TOKEN")
