import discord
from discord import app_commands
from discord.ext import commands
import wiki_manager

# here specify the main command as name
async def setup(bot):

    @bot.tree.command(name="wiki", description="Returns the closest wiki searches")
    @app_commands.describe(query = "Your search query on wikipedia")
    async def wiki(interaction: discord.Interaction, query: str):
        await wiki_manager.wiki(query, interaction.channel)

    @bot.tree.command(name="chem", description="Displays basic data about given chemicals")
    @app_commands.describe(chemicals = "Chemical names")
    async def chem(interaction: discord.Interaction, chemicals: str):
        chem_list = chemicals.split(",")
        await wiki_manager.chem(chem_list, interaction.channel, interaction.user)
    
    @bot.tree.command(name="wolfram", description="Returns an answer from the Wolfram API given user input question")
    @app_commands.describe(question = "Question that you want to ask Wolfram")
    async def wolfram(interaction: discord.Interaction, question: str):
        await wiki_manager.wolfram(question, interaction.channel, interaction.user)


        

        



