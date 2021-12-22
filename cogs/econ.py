import sqlite3
import discord
from discord.ext import commands
import random
import aiosqlite

class econ(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready():
        db = await aiosqlite.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\econ_database.db")
        cursor = db.cursor()
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS econ(
            user INTEGER,
            balance INTEGER
            )
        """)
        await db.commit()
        await cursor.close()
        await db.close()

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
    async def balance(self, ctx, user: discord.User = None):
        if user == None:
            user = ctx.author

        db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\econ_database.db")
        cur = db.cursor()
        cur.execute(f"SELECT balance FROM econ WHERE user = {user.id}")
        result = cur.fetchone()
        if result == None:
            await ctx.send("You need to create a profile with z.create")
        else:
            cur.execute(f"SELECT balance FROM econ WHERE user = {user.id}")
            result1 = cur.fetchone()[0]
            await ctx.send(f"{user} has **{result1}** coins")
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

    @commands.command(aliases = ["cf", "flip"], help = "Bet money on flip. z.flip <amount> <side>")
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def coinflip(self, ctx, num: int, arg = None):
    # arg = heads or tails. num = amount betting
        if arg in ["heads", "head", "h", None]:
            arg = "heads"
        elif arg in ["tails", "tail", "t"]:
            arg = "tails"
        else:
            await ctx.send("That isn't an option")
            pass

        db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\econ_database.db")
        cur = db.cursor()
        cur.execute(f"SELECT user FROM econ WHERE user = {ctx.author.id}")
        result = int(cur.fetchone()[0])
        if result == None:
            await ctx.send("You need to create a profile with z.create")
        
        if int(num) < 0:
            await ctx.send("Can't flip negative numbers bud")
        elif int(num) > result:
            await ctx.send("You don't have that much money")
        elif int(num) <= result:
            side = random.choice(["heads", "tails"])
            if side[0] == arg:
                cur.execute(f"UPDATE econ SET balance = balance + {num} WHERE user = {ctx.author.id}")
                db.commit()
                cur.close()
                db.close()
                await ctx.send(f"The coin landed on {side}. You won {num} coins")
            else:
                cur.execute(f"UPDATE econ SET balance = balance - {num} WHERE user = {ctx.author.id}")
                db.commit()
                cur.close()
                db.close()
                await ctx.send(f"The coin landed on {side}. You lost {num} coins")

def setup(bot):
    bot.add_cog(econ(bot))