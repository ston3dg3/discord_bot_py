# Function that initializes all required elements for the bot
from database_test import create_fonts_table, create_message_table, requestAllFonts
from fonts import MyFont

def initialize():
    create_fonts_table()
    create_message_table()
    [MyFont.add_local_font(row) for row in requestAllFonts()]