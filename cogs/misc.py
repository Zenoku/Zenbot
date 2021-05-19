import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandOnCooldown
from discord.ext.commands.cooldowns import BucketType

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        latency = self.client.latency * 1000
        latency_round = round(latency,2)
        await ctx.send(f"{latency_round}ms")

    @commands.command(aliases = ["hello", "hai"])
    async def hi(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}")

    @commands.command(aliases = ["bai"])
    async def bye(self, ctx):
        await ctx.send(f"Bye {ctx.author.name}")

    @commands.command(aliases = ["e"])
    async def echo(self, ctx, *, arg = None):
        if arg == None:
            await ctx.send("Can't send nothing bud")
        else:
            await ctx.send(arg)
    
    @commands.command(aliases = ["fb"])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def feedback(self, ctx, *, arg = None):
        if arg == None:
            await ctx.send("Can't send nothing bud")
        else:
            feedback_channel = self.client.get_channel(840975059312181248)
            await feedback_channel.send(f"**{arg}** submitted by {ctx.author}. Message link: {ctx.message.jump_url}")
            await ctx.send("Feedback submitted")


    @feedback.error
    async def feedback_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("You're on cooldown. Chill out")
        else:
            await ctx.send("Please report this error with z.fb along with how you got it")


    @commands.command()
    async def dm(self, ctx, member:discord.User, *, arg,):
        await member.send(f"**{ctx.author}** says: {arg}")
        await ctx.send("DM sent")

def setup(client):
    client.add_cog(Misc(client))