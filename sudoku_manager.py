from embed_manager import ListEmbed, EmptyEmbed
from sudoku import Sudoku
from ANSI_colours import ANSI
import utilities

# helper function
def sudokuEmbed(sdk: Sudoku):
    stringer = sdk.prettyPrint()
    newstr = ANSI.wrapANSIblock(stringer)
    embed= EmptyEmbed(title=f"Sudoku size: {sdk.side}x{sdk.side} Difficulty: {sdk.difficulty}", description=newstr, color=0x42f56f)
    return embed

async def sudokuCreate(sdk_size: int, sdk_difficulty: int, channel):
    size = utilities.clamp(sdk_size, 2, 10)
    difficulty = utilities.clamp(sdk_difficulty, 10, 80)
    sdk = Sudoku(size, difficulty)
    await channel.send(embed=sudokuEmbed(sdk))

async def sudokuList(channel):
    # generate dict for ListEmbed:
    dicto = {}
    if len(Sudoku.sudoku_list) == 0:
        await channel.send("There are no saved sudoku baords :(")
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
        await channel.send(embed=ListEmbed("Saved Sudoku Boards", dicto, color = 0xffd152))

        
# outputs noError: embed, Error: None
async def sudokuInsert(group: int, square: int, num: int, channel):
    try:
        sdk = Sudoku.sudoku_list[-1] 
        sdk.inputNum(group,square,num)
        await channel.send(embed=sudokuEmbed(sdk))
    except IndexError as err:
        await channel.send("Index Error!")
    
async def sudokuLoad(choice_index, channel):
    # convert to programming counting
    choice_index = choice_index - 1
    choice_index = utilities.clamp(choice_index, 0, len(Sudoku.sudoku_list))
    sdk = Sudoku.sudoku_list[choice_index]
    await channel.send(embed=sudokuEmbed(sdk))

async def sudokuSave(channel):
    sdk = Sudoku.sudoku_list[-1]
    sdk.store()
    strr = f"Successfully saved Sudoku with ID: <{sdk.key}>\nView it with: /sudoku list"
    embed=EmptyEmbed(title="Sudoku Saved", description=strr, color=0x42f56f)
    await channel.send(embed=embed)
    
async def sudokuHelp(channel):
    dictt = {
        "/sudoku help" : "Displays this help message",
        "/sudoku list" : "Lists all saved Sudoku boards and their indices",
        "/sudoku new [size] [difficulty]" : "creates a new Sudoku board",
        "/sudoku load [index]" : "Loads the Sudoku at specified index",
        "/sudoku save": "Saves the current Sudoku board for later",
        "/sudoku insert [group] [square] [number]" : "inserts the number at specified position"
        }
    embed=ListEmbed(title="Sudoku Help Page", value_desc_dict=dictt)
    await channel.send(embed=embed)
