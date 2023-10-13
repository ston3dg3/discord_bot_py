# Function that initializes all required elements for the bot
from database_test import create_fonts_table, create_message_table, create_sudoku_table, requestAllFonts, fetchSudoku
from fonts import MyFont
from sudoku import Sudoku
import pickle

def initialize():
    create_fonts_table()
    create_message_table()
    create_sudoku_table()
    
# fill local sudoku list
    [Sudoku.addBoard(pickle.loads(row[1])) for row in fetchSudoku()]
# fill local font list
    [MyFont.add_local_font(row) for row in requestAllFonts()]



