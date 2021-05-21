import discord
from discord.ext import commands
import os
from discord.ext.commands.errors import CommandOnCooldown
from dotenv import load_dotenv

# bot status
activity = discord.Activity(name="Zenoku fail at coding", type=discord.ActivityType.watching)

# regular bot stuff
client = commands.Bot(command_prefix=["z.", "Z."], case_insensitive=True, activity = activity) 
client.load_extension('jishaku')
# client.remove_command("help")

# .env stuff
load_dotenv()
Token = os.getenv("Token")

# loading events
@client.event
async def on_connect():
    print("Zenbot is connected to Discord")

@client.event
async def on_ready():
    print("Zenbot is ready")

"""
# cooldown error msg
@client.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.Command0nCooldown):
        await ctx.send("You're on a cooldown")
    else:
        await ctx.send("Please report the bug with z.fb")
"""

"""
work on embeds and stuff. also uncomment remove(help) above when done

@client.command()
async def help(ctx):
    await ctx.send("Work In Progress, commands are hi, bye, and feedback for now")
"""

# loading cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(Token)