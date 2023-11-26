from discord import Interaction, app_commands
from discord.ext import commands
import font_manager

# here specify the main command as name
async def setup(bot):
    grp = FontSlash(name="font", description="Font styling commands")
    bot.tree.add_command(grp)


class FontSlash(app_commands.Group):

    @app_commands.command(name="list", description="List all existing fonts")
    async def list(self, interaction: Interaction):
        await interaction.response.send_message(font_manager.listFonts())
    
    @app_commands.command(name="help", description="Help page for the /font command")
    async def list(self, interaction: Interaction):
        await interaction.response.send_message(font_manager.helpFonts())
    
    @app_commands.command(name="style", description="List all existing fonts")
    @app_commands.describe(font_name = "Name of existing font. List fonts using /font list", content = "Message to translate into the specified font")
    async def list(self, interaction: Interaction, font_name: str, content: str):
        await interaction.response.send_message(font_manager.styleFonts(font_name, content)) 
    
    @app_commands.command(name="add", description="List all existing fonts")
    @app_commands.describe(font_name = "Name of the new font to add", alphabet = "FORMAT: <abcdefghijklmnoprstuwvxyz>, adds new font with specified alphabet")
    async def list(self, interaction: Interaction, font_name: str, alphabet: str):
        await interaction.response.send_message(font_manager.addFont(font_name, alphabet))
