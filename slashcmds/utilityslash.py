from discord import Interaction, app_commands
from discord.ext import commands
import utility_manager

# here specify the main command as name
async def setup(bot):

    @bot.tree.command(name="save", description="Saves the message that you reply to")
    async def save(interaction: Interaction):
        await utility_manager.save(interaction.message, interaction.usr, interaction.channel)

    @bot.tree.command(name="viewsaved", description="Displays all saved messages and their coutns")
    async def viewSaved(interaction: Interaction):
        await utility_manager.viewSaved(interaction.channel)
    
    @commands.is_owner()
    @bot.tree.command(name="clear", description="Clears a number of messages from the channel")
    @app_commands.describe(number = "number of messages to delete")
    async def clear(interaction: Interaction, number: int):
        await utility_manager.clear(number, interaction.channel)


        

        



