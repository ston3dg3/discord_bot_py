from discord.ext import commands
import bot_setup
import wiki_manager

async def setup(bot):
    if (bot_setup.load_ext):
        await bot.add_cog(WikiCog(bot))

class WikiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wiki')
    async def wiki(self, ctx, search_term: str):
        await ctx.send(embed = wiki_manager.wiki(search_term, ctx.message.channel))

    @commands.command(name='chem')
    async def chem(self, ctx, *args):
        await ctx.send(wiki_manager.chem(args, ctx.message.author))

    @commands.command(name='wolfram')
    async def wolfram(self, ctx, question: str):
        await ctx.send(wiki_manager.wolfram(question, ctx.message.author))