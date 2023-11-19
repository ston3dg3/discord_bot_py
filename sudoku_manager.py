import discord
from embed_manager import ListEmbed
from sudoku import Sudoku
from ANSI_colours import ANSI
import utilities

# helper function
def sudokuEmbed(sdk: Sudoku):
    stringer = sdk.prettyPrint()
    newstr = ANSI.wrapANSIblock(stringer)
    embed=discord.Embed(title=f"Sudoku size: {sdk.side}x{sdk.side} Difficulty: {sdk.difficulty}", description=newstr, color=0x42f56f)
    return embed

def sudokuCreate(sdk_size: int, sdk_difficulty: int):
    size = utilities.clamp(sdk_size, 2, 10)
    difficulty = utilities.clamp(difficulty, 10, 80)
    sdk = Sudoku(size, difficulty)
    # SUdoku created
    return sudokuEmbed(sdk)

def sudokuList():
    # generate dict for ListEmbed:
    dicto = {}
    if len(Sudoku.sudoku_list) == 0:
        return "There are no saved sudoku baords :("
    i = 1
    for sdk in Sudoku.sudoku_list:
        if sdk:
            newstr = ANSI.wrapANSIblock(sdk.prettyPrint())
            line_name = f"{i}) Sudoku size: {sdk.side}x{sdk.side} Difficulty: {sdk.difficulty}"
            dicto.update({line_name : newstr})
            i = i+1
        else:
            # SUDOKU is None
            pass
    if len(dicto) != 0:
        return ListEmbed("Saved Sudoku Boards", dicto, color = 0xffd152)
    else:
        return "There are no saved sudoku baords :("

# outputs noError: embed, Error: None
def sudokuInsert(group: int, square: int, num: int):
    try:
        # TODO: create a way to choose which sudoku u want to edit
        sdk = Sudoku.sudoku_list[-1] 
        sdk.inputNum(group,square,num)
        embed = sudokuEmbed(sdk)
        return embed
    except IndexError as err:
        return None
    
def sudokuLoad():
    # convert to programming counting
    choice_index = choice_index - 1
    choice_index = utilities.clamp(choice_index, 0, len(Sudoku.sudoku_list))
    sdk = Sudoku.sudoku_list[choice_index]
    return sudokuEmbed(sdk)

def sudokuSave():
    sdk = Sudoku.sudoku_list[-1]
    sdk.store()
    strr = f"Successfully saved Sudoku with ID: <{sdk.key}>\nView it with: /sudoku list"
    embed=discord.Embed(title="Sudoku Saved", description=strr, color=0x42f56f)
    return embed
