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

    @commands.command(name='sudoku')
    async def sudoku(self, ctx, *args):
        # define Sudoku channel
        sudoku_channel = bot_setup.messageCountChannel

        cmds = [
            [["list"], []],
            [["help"], []],
            [["new"], ["size:int:10", "difficulty:int:100"]],
            [["load"], ["sudoku_index:int"]],
            [["save"], []],
            [["insert"], ["group:int", "square:int", "num:int"]]
        ]

        if len(args)>0:
            parsed_args = utilities.parse(cmds, args)
            option = args[0]
            if (option == "list"):
                await sudoku_manager.sudokuList(sudoku_channel)
            elif (option == "help"):
                await sudoku_manager.sudokuHelp(sudoku_channel)
            elif (option == "new"):
                await sudoku_manager.sudokuCreate(parsed_args[0], parsed_args[1], sudoku_channel)
            elif (option == "load"):
                await sudoku_manager.sudokuLoad(parsed_args[0], sudoku_channel)
            elif (option == "save"):
                await sudoku_manager.sudokuSave(sudoku_channel)
            elif (option == "insert"):
                await sudoku_manager.sudokuInsert(parsed_args[0], parsed_args[1], parsed_args[2], sudoku_channel)
            else:
                await sudoku_channel.send(f"Invalid option. Choose one of: [new] [save] [list] or type {bot_setup.bot_prefix}sudoku help")
        else:
            await ctx.send("Not enough input arguments!")




        
        

    