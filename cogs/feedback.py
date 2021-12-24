import discord
from discord.ext import commands
import sqlite3
import datetime
import aiosqlite

class feedback(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready():
        db = await aiosqlite.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\feedback_database.db")
        cursor = db.cursor()
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback(
            user INTEGER,
            message_id TEXT,
            message TEXT
            )
        """)
        await db.commit()
        await cursor.close()
        await db.close()

    @commands.command(aliases = ["fb"], help = "Give Feedback")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def feedback(self, ctx, *, arg = None):
        if arg == None:
            await ctx.send("Can't send nothing bud")
        else:
            # embed stuff
            embed = discord.Embed(title = ctx.author)
            embed.set_thumbnail(url = ctx.author.avatar.url)
            embed.add_field(name = "User ID", value = ctx.author.id, inline = True)
            embed.add_field(name = "Message Link", value = ctx.message.jump.url, inline = False)
            embed.add_field(name = "Time Submitted", value = datetime.datetime.now(), inline = False)
            embed.add_field(name = "Feedback", value = arg, inline = False)
            feedback_channel = self.bot.get_channel(840975059312181248)
            msg = await feedback_channel.send(embed = embed)
            # database stuff
            db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\feedback_database.db")
            cur = db.cursor()
            sql = ("INSERT INTO feedback(user, message_id, message) VALUES(?,?,?)")
            val = (ctx.author.id, msg.id, arg)
            cur.execute(sql, val)
            db.commit()
            cur.close()
            db.close()
            await ctx.send("Feedback submitted")

    # message ids 858125769950494730 and 858126028315689001 are not resolving for some reason
    @commands.command(aliases = ["fbr"], help = "Resolving feedback, need to have message id")
    async def feedbackresolve(self, ctx, *, arg):
        # arg is message id
        if await self.bot.is_owner(ctx.author):
            db = sqlite3.connect(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\feedback_database.db")
            cur = db.cursor()
            cur.execute(f"SELECT user FROM feedback WHERE message_id = {arg}")
            # result is the user id
            result = cur.fetchone()[0]
            if result == None:
                await ctx.send("That feedback doesn't exist")
            else:
                user = self.bot.get_user(result)
                await user.send("Feedback Completed")
                await ctx.send("Feedback Completed")
                # in the future, should prob add embed and specify which feedback im resolving
                cur.execute(f"DELETE FROM feedback WHERE message_id = {arg}")
                channel = self.bot.get_channel(840975059312181248)
                msg = await channel.fetch_message(arg)
                await msg.delete()
                db.commit()
                db.close()

def setup(bot):
    bot.add_cog(feedback(bot))