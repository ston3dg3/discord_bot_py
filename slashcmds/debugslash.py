import discord
from discord import app_commands
from discord.ext import commands
import utility_manager

# here specify the main command as name
async def setup(bot):

    @commands.is_owner()
    @bot.tree.command(name="reload", description="reloads cogs for the bot")
    async def reload(interaction: discord.Interaction, cog: str):
        await bot.reload_extension(f"cogs.{cog.lower()}")
        await interaction.response.send_message(f"extension **{cog.lower()}** reloaded", ephemeral=True)
    
    @commands.is_owner()
    @bot.tree.command(name="unload", description="unloads cogs for the bot")
    async def unload(interaction: discord.Interaction, cog: str):
        await bot.unload_extension(f"cogs.{cog.lower()}")
        await interaction.response.send_message(f"extension **{cog.lower()}** unloaded", ephemeral=True)

    @commands.is_owner()
    @bot.tree.command(name="load", description="loads cogs for the bot")
    async def load(interaction: discord.Interaction, cog: str):
        await bot.load_extension(f"cogs.{cog.lower()}")
        await interaction.response.send_message(f"extension **{cog.lower()}** loaded", ephemeral=True)
