from discord import Interaction, app_commands
import sudoku_manager

# here specify the main command as name
async def setup(bot):
    grp = SudokuSlash(name="sudoku", description="Sudoku game commands")
    bot.tree.add_command(grp)


class SudokuSlash(app_commands.Group):

    @app_commands.command(name="list", description="List all sudoku boards")
    async def list(self, interaction: Interaction):
        await interaction.response.send_message(embed = sudoku_manager.sudokuList())

    @app_commands.command(name="new", description="Create new sudoku")
    @app_commands.describe(size = "Sudoku size. Range [2-10]. Default 3", difficulty = "Easiest: [10], Hardest: [80]. Default 70")
    async def new(self, interaction: Interaction, size:int=3, difficulty:int=70): 
        await interaction.response.send_message(embed = sudoku_manager.sudokuCreate(size, difficulty))

    @app_commands.command(name="load", description="Load an existing sudoku to Discord")
    @app_commands.describe(choice_index = "Index of the sudoku that you want to continue solving")
    async def load(self, interaction: Interaction, choice_index: int):
        await interaction.response.send_message(embed = sudoku_manager.sudokuLoad(choice_index))

    @app_commands.command(name="save", description="Save current sudoku for later")
    async def save(self, interaction: Interaction):
        await interaction.response.send_message(embed = sudoku_manager.sudokuSave())
        
    @app_commands.command(name="insert", description="Insert numbers into Sudoku board")
    async def insert(self, interaction: Interaction, group:int, square:int, num:int): 
        await interaction.response.send_message(embed = sudoku_manager.sudokuInsert(group, square, num))

    @app_commands.command(name="help", description="Explains how to use this command")
    async def help(self, interaction: Interaction): 
        await interaction.response.send_message(embed = sudoku_manager.sudokuHelp())
    



