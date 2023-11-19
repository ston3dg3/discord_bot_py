import bot_setup
from embed_manager import ListEmbed, EmptyEmbed
from fonts import MyFont
import utilities
from database_test import addFont

# generate a dictionary for command help messages and sends an embed with this info
def helpFonts(channel):
    dictt = {
        f"{bot_setup.bot_prefix}font <font_name> <message>" : "Convert your text into a font-styled message",
        f"{bot_setup.bot_prefix}font fonts" : "Displays available fonts",
        f"{bot_setup.bot_prefix}font add <new_font_name> <abcdefghijklmnoprstuwvxyz>" : "Adds new font with the name <new_font_name>. Make sure to put your font letters in the exact order as specified in this help message"
    }
    embed = ListEmbed("Fonts Help Page 🇦 🈂️ 🈺", dictt)
    return embed

# lists all fonts
def listFonts():
    newstr = "\n".join(MyFont.fancy_font_names())
    embed=EmptyEmbed(title="Available Fonts:", description=newstr, color=0xffff)
    return embed

# sends a message in a selected font style (content is the message)
def styleFonts(font_name, content):
    if(font_name in MyFont.font_names()):
        return MyFont.translator(content, font_name=font_name)
    else:
        return content
    
# adds the font of the pasted alphabet with the specified font_name
def addFonts(font_name, alphabet):
    message = MyFont.add_local_font(addFont(font_name=font_name, alphabet=alphabet))
    return message