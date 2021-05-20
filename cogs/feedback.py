import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandOnCooldown
from discord.ext.commands.cooldowns import BucketType

class feedback(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["fb"])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def feedback(self, ctx, *, arg = None):
        if arg == None:
            await ctx.send("Can't send nothing bud")
        else:
            feedback_channel = self.client.get_channel(840975059312181248)
            await feedback_channel.send(f"**{ctx.author}** submits: {arg}. Message link: {ctx.message.jump_url}")
            await ctx.send("Feedback submitted")

    """
    work on feedback resolve command later. prob hav like reactions and embeds and stuff
    @commands.command(aliases = ["fbr"])
    async def feedbackresolve(self, ctx, *, )
    """

    @feedback.error
    async def feedback_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            timeout = round(error.retry_after, 2)
            await ctx.send(f"You're on cooldown. You can use this command in **{timeout}** seconds")
        else:
            await ctx.send("Please report this error with z.fb along with how you got it")

def setup(client):
    client.add_cog(feedback(client))