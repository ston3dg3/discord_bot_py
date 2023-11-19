import sqlite3
from settings import BASE_DIR
import exceptions


def sqlConn(func):
    def wrapper(*args, **kwargs):
        con = sqlite3.Connection(BASE_DIR / "example.db")
        cur = con.cursor()
        result = func(cur, *args, **kwargs)
        con.commit()
        con.close()  
        return result
    return wrapper

############# TABLE INITALIZERS ##################################

@sqlConn
def create_message_table(cur):
    # Create the 'message_counts' table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS saved_mgs (
                  message TEXT PRIMARY KEY,
                  count INT
                )''')
    
@sqlConn
def create_fonts_table(cur):
    # Create the 'message_counts' table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS saved_fonts (
                  name TEXT PRIMARY KEY,
                  alphabet INT
                )''')
    
@sqlConn
def create_sudoku_table(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS saved_sudoku (
                  id TEXT PRIMARY KEY,
                  board INT
                )''')

    
################## TABLE DELETERS ############################


@sqlConn
def clear_table(cur):
    # delete the whole table for testing
    cur.execute(""" DELETE FROM saved_mgs """)

@sqlConn
def deleteSudokus(cur):
    # delete the whole table for testing
    cur.execute(""" DELETE FROM saved_sudoku """)


@sqlConn
def deleteNoneTypes(cur):
    # delete all rows from the table that are of type None
    cur.execute(""" DELETE FROM saved_mgs WHERE message IS NULL """)


####################### TABLE UPDATES ############################


@sqlConn
def updateMessage(cur, msg):
    if msg is None: raise exceptions.DatabaseNoneType

    # Check if the message is in the database
    cur.execute('SELECT * FROM saved_mgs WHERE message = ?', (msg,))
    row = cur.fetchone()

    if row is None:
        # If the message is not in the database, insert it with a count of 1
        cur.execute('INSERT INTO saved_mgs (message, count) VALUES (?, 1)', (msg,))
    else:
        # If the message is in the database, update the count
        new_count = row[1] + 1
        cur.execute('UPDATE saved_mgs SET count = ? WHERE message = ?', (new_count, msg))

@sqlConn
def addFont(cur, font_name, alphabet):
    if font_name is None or alphabet is None: raise exceptions.DatabaseNoneType
    
    # Check if the message is in the database
    cur.execute('SELECT * FROM saved_fonts WHERE name = ?', (font_name,))
    row = cur.fetchone()

    if row is None:
        # If the font is not in the database, insert it with value alphabet
        cur.execute('INSERT INTO saved_fonts (name, alphabet) VALUES (?, ?)', (font_name,alphabet))
        return row
    else:
        # If the font is in the database, return error message
        error_message = "Such font name already exists. Check the font command for details"
        return error_message
    

@sqlConn
def updateSudoku(cur, serial_sudoku, sudoku_ID):
    if serial_sudoku is None or sudoku_ID is None: raise exceptions.DatabaseNoneType

    # Check if the sudoku ID is in the database
    cur.execute('SELECT * FROM saved_sudoku WHERE id = ?', (sudoku_ID,))
    row = cur.fetchone()

    if row is None:
        # If the sudoku is not in the database, insert it with value serialized
        cur.execute('INSERT INTO saved_sudoku (id, board) VALUES (?, ?)', (sudoku_ID,serial_sudoku))
    else:
        # If sudoku is in the database, update it
        cur.execute('UPDATE saved_sudoku SET board = ? WHERE id = ?', (serial_sudoku, sudoku_ID))



######################## TABLE FETCH REQUESTS #########################

@sqlConn
def fetchData(cur):
    cur.execute('SELECT * FROM saved_mgs')
    rows = cur.fetchall()
    return rows

# @sqlConn
# def requestFont(cur, font_name):
#     cur.execute('SELECT * FROM saved_fonts WHERE name = ?', (font_name,))
#     row = cur.fetchone()
#     return row

@sqlConn
def requestAllFonts(cur):
    cur.execute('SELECT * FROM saved_fonts')
    rows = cur.fetchall()
    return rows

@sqlConn
def fetchSudoku(cur):
    cur.execute('SELECT * FROM saved_sudoku')
    rows = cur.fetchall()
    return rows


#######################################################################

# deleteNoneTypes()
# deleteSudokus()