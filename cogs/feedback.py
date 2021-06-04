import discord
from discord.ext import commands
import sqlite3
from sqlite3 import Error


class feedback(commands.Cog):

    def __init__(self, client):
        self.client = client

    # stuff for feedback database. not exactly sure if it should be in the feedback class

    # connecting to database
    def create_connection(path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    connection = create_connection(r"C:\Users\Admin\Desktop\Python Programs\Projects\Zenbot\databases\feedback_database.db")

    def execute_query(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    create_feedback_table = """
    CREATE TABLE IF NOT EXISTS feedback (
        User INTEGER
        Feedback TEXT
    );
    """

    execute_query(connection, create_feedback_table)


    @commands.command(aliases = ["fb"])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def feedback(self, ctx, *, arg = None):
        if arg == None:
            await ctx.send("Can't send nothing bud")
        else:
            embed = discord.Embed(title = ctx.author)
            embed.add_field(name = "User ID", value = ctx.author.id, inline = True)
            embed.add_field(name = "Feedback", value = arg, inline = False)
            embed.add_field(name = "Message Link", value = ctx.message.jump_url, inline = False)
            feedback_channel = self.client.get_channel(840975059312181248)
            await feedback_channel.send(embed = embed)
            # database stuff
            create_feedback = """
            INSERT INTO
                feedback (User, Feedback)
            VALUES
                (ctx.author.id, 'arg')
            """
            await ctx.send("Feedback submitted")

    @feedback.error
    async def feedback_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            timeout = round(error.retry_after, 2)
            await ctx.send(f"You're on cooldown. You can use this command in **{timeout}** seconds")
        else:
            await ctx.send("Please report this error with z.fb along with how you got it")

    """
    work on feedback resolve command later. prob hav like reactions and embeds and stuff
    @commands.command(aliases = ["fbr"])
    async def feedbackresolve(self, ctx, *, arg)
    """

def setup(client):
    client.add_cog(feedback(client))