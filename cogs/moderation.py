import discord
from discord.ext import commands

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # command is decorator for cogs
    @commands.command(aliases = ["sb"], help = "For banning yourself")
    async def selfban(self, ctx):
        await ctx.guild.ban(ctx.author, reason = f"{ctx.author} banned themself", delete_message_days = 0)
        await ctx.send(f"{ctx.author} has banned themself")

    @commands.command(aliases = ["ub"], help = "Unban someone")
    async def unban(self, ctx, user: discord.User):
        if ctx.author.guild_permissions.ban_members:
            await ctx.guild.unban(user)
            await user.send(f"You have been unbanned from {ctx.guild}")
            await ctx.send(f"{user} has been unbanned")
        else:
            await ctx.send("You don't have the permissions to do this")

    @commands.command(aliases = ["sk"], help = "For kicking yourself")
    async def selfkick(self, ctx):
        await ctx.guild.kick(ctx.author)
        await ctx.send(f"{ctx.author} has kicked themself")
    
    @commands.command(help = "Deletes messages in a channel")
    async def clear(self, ctx, arg):
        if ctx.author.guild_permissions.manage_messages:
            num = int(arg) + 1
            await ctx.channel.purge(limit = num)
        else:
            await ctx.send("You don't have the permmissions to do this")

def setup(bot):
    bot.add_cog(moderation(bot))