from discord.ext import commands
import utilities
import bot_setup
import font_manager

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

        if(len(args)>0):
            # decide what to do based on chosen command
            if(args[0] == "list"):
                await ctx.send(embed = font_manager.listFonts())
                return
            elif(args[0] == "help"):
                await ctx.send(embed=font_manager.helpFonts())
                return
            elif(args[0] == "add"):
                font_name = parsed_args[0]
                alphabet = parsed_args[1]
                font_manager.addFonts(font_name, alphabet)
                return
            elif(args[0] == "style"):
                font_name = parsed_args[0]
                content = parsed_args[1]
                await ctx.send(font_manager.styleFonts(font_name, content))
                await ctx.message.delete()
                return
        else:
            await ctx.send("Not enough input arguments!")