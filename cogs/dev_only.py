import discord
from discord.ext import commands

class dev_only(commands.Cog):
    
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
            await ctx.send("Lmao you thought")
    
    # listing the number of servers + what severs r in
    @commands.command()
    async def serverlist(self, ctx):
        if await self.client.is_owner(ctx.author):
	        await ctx.send(f"In **{len(list(self.client.guilds))}** servers\nServer info: {list(self.client.guilds)}")
        else:
            await ctx.send("Lmao you thought")
    
    # for writing in channels without using echo
    @commands.command()
    async def speak(self, ctx, *, arg):
        if await self.client.is_owner(ctx.author):
            channel = self.client.get_channel(708689179831435326)
            await channel.send(arg)
        else:
            await ctx.send("Lmao you thought")

def setup(client):
    client.add_cog(dev_only(client))