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
            # EXCEPTION: returns a string, not an Embed
            elif(args[0] == "add"):
                font_name = parsed_args[0]
                alphabet = parsed_args[1]
                message_str = font_manager.addFonts(font_name, alphabet)
                await ctx.send(message_str)
                return
            # EXCEPTION: returns a string, not an Embed
            elif(args[0] == "style"):
                font_name = parsed_args[0]
                content = parsed_args[1]
                message_str = font_manager.styleFonts(font_name, content)
                await ctx.send(message_str)
                await ctx.message.delete()
                return
        else:
            error_str = "Not enough input arguments!"
            await ctx.send(error_str)