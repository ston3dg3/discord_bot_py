import discord
from discord.ext import commands

from embed_manager import ListEmbed
from customUI import MyButtonView, MySelectView
from database_test import fetchData
import scraper
import json
from API_requests import requestHandler
import bot_setup


async def setup(bot):
    if (bot_setup.load_ext):
        await bot.add_cog(WikiCog(bot))

class WikiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class wikiFlags(commands.FlagConverter):
        search_term: str = commands.flag(description="Insert a topic that you want to search on Wikipedia")


    @commands.hybrid_command(name='wiki')
    async def wiki(self, ctx, *, flags: wikiFlags):
        query = flags.search_term
        results = scraper.wikiScraper.wikiSearches(query)
        if not results:
                await ctx.send("What are you on about u dummy? 😤")
                return
        results = [discord.SelectOption(label=result, value=result) for result in results]
        view = MySelectView(ctx)
        view.add_select_options(options=results)
        await ctx.send(view=view)
        await view.wait()
        embed=discord.Embed(title=view.sel_opt, description=view.summary, color=0xff33cc)
        await ctx.send(embed=embed)
        view.clear_items()

    # @commands.hybrid_command(name='chem')
    # async def chem(self, ctx, *args: commands.Greedy[str]):
    #     chem_list_to_display = scraper.wikiScraper.wikiSearchResults(args, bot_setup.chem_attributes_list)
    #     usr = ctx.message.author
    #     for chemical in chem_list_to_display:
    #         embed=discord.Embed(title=chemical.query, description=chemical.content, color=usr.accent_color, url=chemical.url)
    #         await ctx.send(embed=embed)


    class wolframFlags(commands.FlagConverter):
        search_term: str = commands.flag(description="Insert a question for the Wolfram engine")


    @commands.hybrid_command(name='wolfram')
    async def wolfram(self, ctx, question: wolframFlags):
        query = '+'.join(question)
        response = requestHandler(query).API_getWolfram()
        usr = ctx.message.author
        
        if response.status_code == 501:
            await ctx.send("That's some gibberish right there 👀🧃")
            return
        try:
            text_response = json.loads(response.text)["result"]
            question = ' '.join(question)
            embed=discord.Embed(title=question, description=text_response, color=usr.accent_color)
            embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("That's some gibberish right there 👀🧃\nYou gotta be more precise next time 😊")
