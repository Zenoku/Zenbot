import discord
from discord.ext import commands
import os
from discord.ext.commands.bot import when_mentioned_or
from dotenv import load_dotenv
import platform
import sqlite3

# intent stuff
intents = discord.Intents.default()
intents.members = True

# bot status
activity = discord.Activity(name = "Zenoku fail at coding", type = discord.ActivityType.watching)

# regular bot stuff
bot = commands.Bot(command_prefix = when_mentioned_or("z.", "Z."), case_insensitive = True, intents = intents, activity = activity) 
bot.load_extension("jishaku")

# .env stuff
load_dotenv()
Token = os.getenv("Token")

# loading event
@bot.event
async def on_ready():
    # feedback database
    db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\feedback_database.db")
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
        user INTEGER,
        message_id TEXT,
        message TEXT
        )
    """)
    db.commit()
    cursor.close()
    db.close()
    # econ database
    db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\econ_database.db")
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS econ(
        user INTEGER,
        balance INTEGER
        )
    """)
    db.commit()
    cursor.close()
    db.close()
    # non-database stuff
    print("-------")
    print("Bot online")
    print(f"Discord.py Version: {discord.__version__}")
    print(f"Python Version: {platform.python_version()}")
    print(f"SQLite Version: {sqlite3.version}")
    print("-------")

# runs edited messages
@bot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        await bot.on_message(after)


# error msges
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing something bud")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("That command has been disabled")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("That command isn't for you")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You're missing {error.missing_perms} to use that command")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f"I am missing {error.missing_perms} to use that command")        
    else:
        log_channel = bot.get_channel(845671875626795008)
        embed = discord.Embed(title = "Error Encountered")
        embed.set_thumbnail(url = ctx.author.avatar_url)
        embed.add_field(name = "Encountered by:", value = ctx.author, inline = True)
        embed.add_field(name = "Encountered in server:", value = ctx.guild, inline = True)
        embed.add_field(name = "Message link:", value = ctx.message.jump_url, inline = True)
        # add an encountered at time
        embed.add_field(name = "Error:", value = error, inline = True)
        await log_channel.send(embed = embed)
        await ctx.send("Some error has occured and has been reported")


"""
# needs major improvements but at least it works
class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()
"""

# loading cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(Token)