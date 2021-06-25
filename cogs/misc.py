import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandOnCooldown
from discord.ext.commands.cooldowns import BucketType

class misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help = "Check latency")
    async def ping(self, ctx):
        latency = self.bot.latency * 1000
        latency_round = round(latency,2)
        await ctx.send(f"Pong! {latency_round}ms")

    @commands.command(aliases = ["e"], help = "Bot echos what you say")
    async def echo(self, ctx, *, arg = None):
        if arg == None:
            await ctx.send("Can't send nothing bud")
        else:
            await ctx.send(arg)

    @commands.command(help = "DM someone")
    async def dm(self, ctx, member:discord.User, *, arg,):
        await member.send(f"**{ctx.author}** says: {arg}")
        await ctx.send("DM sent")
    
    @commands.command(help = "Bonk someone")
    async def bonk(self, ctx, member:discord.User):
        await ctx.send(f"**{ctx.author}** bonks **{member}** https://tenor.com/view/kendo-shinai-bonk-doge-horny-gif-20995284")

def setup(bot):
    bot.add_cog(misc(bot))