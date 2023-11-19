from discord.ext import commands
from customUI import MyButtonView, MySelectView
import bot_setup

async def setup(bot):
    if (bot_setup.load_ext):
        await bot.add_cog(ViewCog(bot))

class ViewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def button(self, ctx):
        view = MyButtonView(ctx)
        await ctx.send('Hi', view=view)
        await view.wait()

    @commands.command()
    async def selection(self, ctx):
        view = MySelectView(ctx.message.channel)
        await ctx.send(view=view)

    # # NON WORKING FUNCTION, MIGHT FIX LATER
    # @commands.command(name = "selection")

    # @commands.command(name = "button")
    # async def button(self, ctx):

