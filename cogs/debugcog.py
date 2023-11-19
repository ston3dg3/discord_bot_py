import discord
from discord.ext import commands

from embed_manager import ListEmbed
import bot_setup

async def setup(bot):
    if (bot_setup.load_ext):
        await bot.add_cog(DebugCog(bot))

class DebugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ping(self, ctx):
        # Send a temporary message to measure the round-trip time
        message = await ctx.send("Pinging...")
        # Calculate the round-trip time (latency)
        await message.edit(content=f"Pong 👀🧃 ({self.bot.latency:.2f} ms)")

    @commands.command(name='toggle')
    async def toggle(self, ctx, setting, *args):
        a=3
        # TODO: toggle functon to change bot settings on/off
