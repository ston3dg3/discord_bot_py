import discord
from discord import app_commands
import sudoku_manager

# here specify the main command as name
async def setup(bot):
    grp = SudokuSlash(name="sudoku", description="Sudoku game commands")
    bot.tree.add_command(grp)


class SudokuSlash(app_commands.Group):

    @app_commands.command(name="list", description="List all sudoku boards")
    async def list(self, interaction: discord.Interaction):
        await sudoku_manager.sudokuList(interaction.channel)

    @app_commands.command(name="new", description="Create new sudoku")
    @app_commands.describe(size = "Sudoku size. Range [2-10]. Default 3", difficulty = "Easiest: [10], Hardest: [80]. Default 70")
    async def new(self, interaction: discord.Interaction, size:int=3, difficulty:int=70): 
        await sudoku_manager.sudokuCreate(size, difficulty, interaction.channel)

    @app_commands.command(name="load", description="Load an existing sudoku to Discord")
    @app_commands.describe(choice_index = "Index of the sudoku that you want to continue solving")
    async def load(self, interaction: discord.Interaction, choice_index: int):
        await sudoku_manager.sudokuLoad(choice_index, interaction.channel)

    @app_commands.command(name="save", description="Save current sudoku for later")
    async def save(self, interaction: discord.Interaction):
        await sudoku_manager.sudokuSave(interaction.channel)
        
    @app_commands.command(name="insert", description="Insert numbers into Sudoku board")
    async def insert(self, interaction: discord.Interaction, group:int, square:int, num:int): 
        await sudoku_manager.sudokuInsert(group, square, num, interaction.channel)

    @app_commands.command(name="help", description="Explains how to use this command")
    async def help(self, interaction: discord.Interaction): 
        await sudoku_manager.sudokuHelp(interaction.channel)


# TODO: SUDOKU HELP FUNCTION
    # class sudokuFlags(commands.FlagConverter):
    #     option: str = commands.flag(description="What do you want to do? [new] - Create new Sudoku. [save] - Save current sudoku. [list] - List all sudoku boards")
    #     difficulty: int = commands.flag(description="Easiest: [10], Hardest: [80]. Default 70", default=70)
    #     size: int = commands.flag(description="Sudoku size. Range [2-10]. Default 3", default=3)

        
    # class insertFlags(commands.FlagConverter):
    #     group: int = commands.flag(description='The group number (1-9)')
    #     square: int = commands.flag(description='The square number (1-9)')
    #     num: int = commands.flag(description='The number you want to place')
    #     sdk_choice: int = commands.flag(default=0, description='Which sudoku? Default is last modified')

    



