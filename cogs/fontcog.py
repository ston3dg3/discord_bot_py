import discord
from discord.ext import commands

from fonts import MyFont
from database_test import addFont
from embed_manager import ListEmbed
import utilities
import bot_setup


async def setup(bot):
    if (bot_setup.load_ext):
        await bot.add_cog(FontCog(bot))


# Create a FontCog class for managing the /font command and subcommands
class FontCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def font(self, ctx, *args):
        cmds = [
            [["list"], []],
            [["help"], []],
            [["add"], ["name:str", "alphabet:str:26"]],
            [["style"], ["name", "*message"]]
        ]
        parsed_args = utilities.parse(cmds, args)

        def helpFonts():
            dictt = {
                f"{bot_setup.bot_prefix}font <font_name> <message>" : "Convert your text into a font-styled message",
                f"{bot_setup.bot_prefix}font fonts" : "Displays available fonts",
                f"{bot_setup.bot_prefix}font add <new_font_name> <abcdefghijklmnoprstuwvxyz>" : "Adds new font with the name <new_font_name>. Make sure to put your font letters in the exact order as specified in this help message"
            }
            embed = ListEmbed("Fonts Help Page 🇦 🈂️ 🈺", dictt)
            return embed

        def listFonts():
            newstr = "\n".join(MyFont.fancy_font_names())
            embed=discord.Embed(title="Available Fonts:", description=newstr)
            return embed
        
        def styleFonts():
            font_name = parsed_args[0]
            content = parsed_args[1]
            if(font_name in MyFont.font_names()):
                return MyFont.translator(content, font_name=font_name)
            else:
                return content
            
        def addFonts():
            fontName = parsed_args[0]
            alphabet = parsed_args[1]
            message = MyFont.add_local_font(addFont(font_name=fontName, alphabet=alphabet))
            return message
            

        if(args[0] == "list"):
            await ctx.send(embed = listFonts())
            return
        elif(args[0] == "help"):
            await ctx.send(embed=helpFonts())
            return
        elif(args[0] == "add"):
            addFonts()
            return
        elif(args[0] == "style"):
            await ctx.send(styleFonts())
            await ctx.message.delete()
            return


















