import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    # command is decorator for cogs
    @commands.command(aliases = ["sb"])
    async def selfban(self, ctx):
        await ctx.guild.ban(ctx.author)
        await ctx.send(f"{ctx.author} has banned themself")

    @commands.command(aliases = ["sk"])
    async def selfkick(self, ctx):
        await ctx.guild.kick(ctx.author)
        await ctx.send(f"{ctx.author} has kicked themself")
    
    @commands.command()
    async def clear(self, ctx, arg):
        num = int(arg) + 1
        await ctx.channel.purge(limit = num)

def setup(client):
    client.add_cog(Moderation(client))