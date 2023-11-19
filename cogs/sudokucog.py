import discord
from discord.ext import commands

from embed_manager import ListEmbed
import utilities
from sudoku import Sudoku
import bot_setup
import sudoku_manager

async def setup(bot):
    if (bot_setup.load_ext):
        await bot.add_cog(SudokuCog(bot))

class SudokuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # cmds = [
        #     [["list"], []],
        #     [["help"], []],
        #     [["new"], ["name:str", "alphabet:str:26"]],
        #     [["style"], ["name", "*message"]]
        # ]

    class sudokuFlags(commands.FlagConverter):
        option: str = commands.flag(description="What do you want to do? [new] - Create new Sudoku. [save] - Save current sudoku. [list] - List all sudoku boards")
        difficulty: int = commands.flag(description="Easiest: [10], Hardest: [80]. Default 70", default=70)
        size: int = commands.flag(description="Sudoku size. Range [2-10]. Default 3", default=3)

    @commands.hybrid_command(name='sudoku')
    async def sudoku(self, *, flags: sudokuFlags):

        sudoku_channel = bot_setup.messageCountChannel

        if (flags.option == "new"):
            await sudoku_channel.send(embed = sudoku_manager.sudokuCreate(flags.size, flags.difficulty))
        elif (flags.option == "save"):
            await sudoku_channel.send(embed = sudoku_manager.sudokuSave())
        elif (flags.option == "list"):
            await sudoku_channel.send(embed = sudoku_manager.sudokuList())            
        else:
            await sudoku_channel.send("Invalid option. Choose one of: [new] [save] [list]")

    class insertFlags(commands.FlagConverter):
        group: int = commands.flag(description='The group number (1-9)')
        square: int = commands.flag(description='The square number (1-9)')
        num: int = commands.flag(description='The number you want to place')
        sdk_choice: int = commands.flag(default=0, description='Which sudoku? Default is last modified')


    @commands.hybrid_command(name='insert')
    async def insert(self, ctx, *, flags: insertFlags):
        sudoku_channel = bot_setup.messageCountChannel
        my_inserted_sudoku = sudoku_manager.sudokuInsert(flags.group, flags.square, flags.num)
        await sudoku_channel.send(embed=my_inserted_sudoku)
        
        

    