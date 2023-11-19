import discord
from discord import app_commands
import sudoku_manager

# here specify the main command as name
async def setup(bot):
    grp = SudokuSlash(name="sudoku", description="Sudoku game commands")
    bot.tree.add_command(grp)


class SudokuSlash(app_commands.Group):

    @app_commands.command()
    async def list(self, interaction: discord.Interaction):
        my_sdk_list = sudoku_manager.sudokuList()
        await interaction.response.send_message(embed=my_sdk_list)

    @app_commands.command()
    async def new(self, interaction: discord.Interaction, size:int, difficulty:int):
        my_new_sdk = sudoku_manager.sudokuCreate(size, difficulty)
        await interaction.response.send_message(embed=my_new_sdk)

    @app_commands.command()
    async def load(self, interaction: discord.Interaction):
        my_loaded_sdk = sudoku_manager.sudokuLoad()
        await interaction.response.send_message(embed=my_loaded_sdk)

    @app_commands.command()
    async def save(self, interaction: discord.Interaction):
        my_saved_sdk = sudoku_manager.sudokuSave()
        await interaction.response.send_message(embed=my_saved_sdk)
        
    @app_commands.command()
    async def insert(self, interaction: discord.Interaction):
        my_inserted_sdk = sudoku_manager.sudokuInsert()
        await interaction.response.send_message(embed=my_inserted_sdk)
        

        



