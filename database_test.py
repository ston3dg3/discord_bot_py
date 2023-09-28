import sqlite3


def sqlConn(func):
    def wrapper(*args, **kwargs):
        con = sqlite3.Connection("example.db")
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

    
################## TABLE DELETERS ############################


@sqlConn
def clear_table(cur):
    # delete the whole table for testing
    cur.execute(""" DELETE FROM saved_mgs """)


####################### TABLE UPDATES ############################


@sqlConn
def updateMessage(cur, msg):
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


#######################################################################