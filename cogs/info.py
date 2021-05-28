import discord
from discord.ext import commands

class info(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases = ["ui"])
    async def userinfo(self, ctx, member:discord.User = None):
        if member == None:
            member = ctx.author

        embed = discord.Embed(title = member, color = member.color)
        embed.add_field(name = "Member ID", value = member.id, inline = True)
        embed.add_field(name = "Creation date", value = member.created_at, inline = True)
        embed.add_field(name = "Color", value = member.color, inline = True)
        embed.set_image(url = member.avatar_url)
        await ctx.send(embed = embed)

    
    # add embeds and figure out role permission stuff
    @commands.command(aliases = ["ri"])
    async def roleinfo(self, ctx, role:discord.Role = None):
        if role == None:
            await ctx.send("You must input a role name or id")
        else:
            await ctx.send(f"**{role}**\nId: {role.id}\nMentionable: {role.mentionable}\nPermissions: {role.permissions}\nColor: {role.color}\nCreated at {role.created_at}")

    @commands.command(aliases = ["si", "gi"])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title = guild)
        embed.add_field(name = "Owner", value = guild.owner, inline = True)
        embed.add_field(name = "ID", value = guild.id, inline = True)
        embed.add_field(name = "Created at", value = guild.created_at, inline = True)
        embed.add_field(name = "Boosts", value = guild.premium_subscription_count, inline = True)
        embed.add_field(name = "Number of channels", value = len(guild.channels), inline = True)
        embed.add_field(name = "Number of members", value = guild.member_count, inline = True)
        # idk why owner isn't returning. debug later
        embed.add_field(name = "Number of roles", value = len(guild.roles), inline = True)
        embed.set_image(url = guild.icon_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ["sc"])
    async def sourcecode(self, ctx):
        await ctx.send("https://github.com/Zenoku/Zenbot")

def setup(client):
    client.add_cog(info(client))