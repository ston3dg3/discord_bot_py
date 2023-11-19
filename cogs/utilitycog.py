import discord
from discord.ext import commands

from embed_manager import ListEmbed
from customUI import MyButtonView, MySelectView
import bot_setup
from database_test import fetchData
from scraper import wikiScraper
import utilities
from API_requests import requestHandler

async def setup(bot):
    if (bot_setup.load_ext):
        await bot.add_cog(UtilityCog(bot))

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='save')
    async def save(self, ctx):
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        saved_channel = bot_setup.savedMessageChannel
        usr = ctx.message.reference.resolved.author
        embed=discord.Embed(title="", description=message.content, color=usr.accent_color)
        embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
        await saved_channel.send(embed=embed)

    @commands.command(name='viewSaved')
    async def viewSaved(self, ctx):

        count_channel = bot_setup.messageCountChannel
        rows = fetchData()
        dictt = None
        if rows:
            dictt = {str(row[0]):str(row[1]) for row in rows}
            embed = ListEmbed("Saved Messages", dictt, color=0xfcba03)
            await count_channel.send(embed=embed)
        else:
            await count_channel.send("No message counts found!")

    @commands.command(pass_context = True, name='clear')
    async def clear(self, ctx, number=1):
        mgs = [] #Empty list to put all the messages in the log
        number = int(number) #Converting the amount of messages to delete to an integer
        number = utilities.clamp(number, 1, 6)

        channel = ctx.message.channel
        async for message in channel.history(limit = number):
            mgs.append(message)
        for message in mgs:
            await message.delete()

   