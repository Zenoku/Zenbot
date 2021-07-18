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
        result = cur.execute(f"SELECT user FROM econ WHERE user = {ctx.author.id}")
        result = cur.fetchone()
        if result == None:
            await ctx.send("You need to create a profile with z.create")
        else:
            await ctx.send(f"You have **{result}** coins")
            cur.close()
            db.close()

    @commands.command()
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

    @commands.command()
    async def coinflip(self, ctx, num, arg):
    # arg = heads or tails. num = amount betting
        if arg != "heads" or "tails":
            await ctx.send("You can only pick either heads or tails")
        await ctx.send("Pleaceholder")

def setup(bot):
    bot.add_cog(econ(bot))