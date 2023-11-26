from discord import Interaction, app_commands
from discord.ext import commands
import wiki_manager
from typing import List

# here specify the main command as name
async def setup(bot):

    @bot.tree.command(name="wiki", description="Returns the closest wiki searches")
    @app_commands.describe(query = "Your search query on wikipedia")
    async def wiki(interaction: Interaction, query: str):
        await interaction.response.send_message(embed = wiki_manager.wiki(query, interaction.channel))

    @bot.tree.command(name="chem", description="Displays basic data about given chemicals")
    @app_commands.describe(chemicals = "Chemical names")
    async def chem(interaction: Interaction, chemicals: str):
        chem_list = chemicals.split(",")
        await interaction.response.send_message(embeds=wiki_manager.chem(chem_list, interaction.channel, interaction.user))
    
    @bot.tree.command(name="wolfram", description="Returns an answer from the Wolfram API given user input question")
    @app_commands.describe(question = "Question that you want to ask Wolfram")
    async def wolfram(interaction: Interaction, question: str):
        await interaction.response.send_message(wiki_manager.wolfram(question, interaction.user))


        

        



