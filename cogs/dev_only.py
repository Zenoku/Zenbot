import discord
from discord.ext import commands

class restricted(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # leaving specific servers
    @commands.command()
    async def serverleave(self, ctx):
        if await self.client.is_owner(ctx.author):
            server_id = "insert server id here"
            server = discord.utils.get(self.client.guilds, id=server_id)
            await server.leave()
            await ctx.send("Left server")
        else:
            await ctx.send("You can't use that command")
    
    # listing the number of servers + what severs r in
    @commands.command()
    async def serverlist(self, ctx):
        if await self.client.is_owner(ctx.author):
	        await ctx.send(f"In **{len(list(self.client.guilds))}** servers\nServer info: {list(self.client.guilds)}")
        else:
            await ctx.send("You can't use that command")

def setup(client):
    client.add_cog(restricted(client))