import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandOnCooldown
from discord.ext.commands.cooldowns import BucketType

"""
always unload this cog when not in use
"""

class dev_only(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # leaving specific servers
    @commands.command()
    async def serverleave(self, ctx):
        server_id = "insert server id here"
        server = discord.utils.get(self.client.guilds, id=server_id)
        await server.leave()
        await ctx.send("Left server")
    
    # listing the number of servers + what severs r in
    @commands.command()
    async def serverlist(self, ctx):
	    await ctx.send(f"In: {len(list(self.client.guilds))} servers\nServer info: {list(self.client.guilds)}")

def setup(client):
    client.add_cog(dev_only(client))