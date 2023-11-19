import discord
from discord.ext import commands

from customUI import MySelectView
import scraper
import json
from API_requests import requestHandler
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
        await wiki_manager.wiki(search_term, ctx.message.channel)

    @commands.command(name='chem')
    async def chem(self, ctx, *args):
        await wiki_manager.chem(args, ctx.message.channel, ctx.message.author)

    @commands.command(name='wolfram')
    async def wolfram(self, ctx, question: str):
        await wiki_manager.wolfram(question, ctx.message.channel, ctx.message.author)