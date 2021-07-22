import sqlite3
import discord
from discord.ext import commands
import random

class econ(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help = "Create your profile")
    async def create(self, ctx):
        db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\econ_database.db")
        cur = db.cursor()
        cur.execute(f"SELECT user FROM econ WHERE user = {ctx.author.id}")
        result = cur.fetchone()
        if result == None:
            sql = ("INSERT INTO econ(user, balance) VALUES(?,?)")
            val = (ctx.author.id, 0)
            cur.execute(sql, val)
            db.commit()
            cur.close()
            db.close()
            await ctx.send("Profile created")
        else:
            await ctx.send("You already have a profile")

    @commands.command(aliases = ["bal", "b"], help = "See your balance")
    async def balance(self, ctx):
        db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\econ_database.db")
        cur = db.cursor()
        cur.execute(f"SELECT balance FROM econ WHERE user = {ctx.author.id}")
        result = cur.fetchone()
        if result == None:
            await ctx.send("You need to create a profile with z.create")
        else:
            cur.execute(f"SELECT balance FROM econ WHERE user = {ctx.author.id}")
            result1 = cur.fetchone()[0]
            await ctx.send(f"You have **{result1}** coins")
            cur.close()
            db.close()

    @commands.command(help = "Claim daily awards")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\econ_database.db")
        cur = db.cursor()
        cur.execute(f"SELECT user FROM econ WHERE user = {ctx.author.id}")
        result = cur.fetchone()
        if result == None:
            await ctx.send("You need to create a profile with z.create")
        else:
            cur.execute(f"UPDATE econ SET balance = balance + 100 WHERE user = {ctx.author.id}")
            db.commit()
            cur.close()
            db.close()
            await ctx.send("You have claimed your daily 100 coins")
    
    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            timeout = round(error.retry_after, 2)
            await ctx.send(f"You're on cooldown. You can use this command in **{timeout}** seconds")

    @commands.command(help = "Generate money. For devs only")
    async def agive(self, ctx, user: discord.User, num):
        if await self.bot.is_owner(ctx.author):
            db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\econ_database.db")
            cur = db.cursor()
            cur.execute(f"SELECT user FROM econ WHERE user = {user.id}")
            result = cur.fetchone()
            if result == None:
                await ctx.send("They don't have a profile")
            else:
                cur.execute(f"UPDATE econ SET balance = balance + {num} WHERE user = {user.id}")
                db.commit()
                cur.close()
                db.close()
                await ctx.send(f"Command successful. Gave {num} to {user}")
        else:
            await ctx.send("Lmao you thought")

    @commands.command()
    async def give(self, ctx, user: discord.User, num):

        await ctx.send("Placeholder")

    @commands.command()
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def coinflip(self, ctx, num = 0, arg = "heads"):
    # arg = heads or tails. num = amount betting
        if num < 0:
            await ctx.send("Can't flip negative numbers bud")
        if arg != "heads" or "tails":
            await ctx.send("You can only pick either heads or tails. This is case sensitive until I figure out how to make it not.")
        
        # finish this later but this is for checking if they are betting over the amount they have
        db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\econ_database.db")
        cur = db.cursor()
        cur.execute(f"SELECT user FROM econ WHERE user = {ctx.author.id}")
        result = cur.fetchone()
        if result == None:
            await ctx.send("They don't have a profile")
        else:
            await ctx.send("Placeholder")

        result = random.choice("heads", "tails")
        if result == arg:
            # insert database stuff
            await ctx.send(f"You won {arg} coins")
        else:
            # insert database stuff
            await ctx.send(f"You lost {arg} coins")
    
    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            timeout = round(error.retry_after, 2)
            await ctx.send(f"You're on cooldown. You can use this command in **{timeout}** seconds")

def setup(bot):
    bot.add_cog(econ(bot))