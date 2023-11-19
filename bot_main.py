import discord
from discord.ext import commands
from discord import app_commands
import settings
import bot_setup
from database_test import create_fonts_table, create_message_table, create_sudoku_table, requestAllFonts, fetchSudoku
from fonts import MyFont
from sudoku import Sudoku
import pickle
import random
import utilities
from database_test import updateMessage

logger = settings.logging.getLogger("bot") 


async def initialize(bot):
    create_fonts_table()
    create_message_table()
    create_sudoku_table()
    # fill local sudoku list
    [Sudoku.addBoard(pickle.loads(row[1])) for row in fetchSudoku()]
    # fill local font list
    [MyFont.add_local_font(row) for row in requestAllFonts()]
    # fetch channel IDs
    def fetchChannel(channelID): return bot.get_channel(channelID) or bot.fetch_channel(channelID)
    bot_setup.messageCountChannel = await fetchChannel(bot_setup.messageCountChannelID)
    bot_setup.savedMessageChannel = await fetchChannel(bot_setup.savedMessageChannelID)


def run():
    bot = commands.Bot(command_prefix=bot_setup.bot_prefix, description=bot_setup.bot_description, intents=bot_setup.getIntents())

    @bot.event
    async def setup_hook():
        # Perform actions after the bot is logged in
        await initialize(bot)

    @bot.event
    async def on_ready():
        logger.info(f"Logged on as User: {bot.user} (ID: {bot.user.id})")        

        # For loading normal commands
        if bot_setup.load_onReady_cmd:
            for cog_file in settings.CMDS_DIR.glob("*.py"):
                if cog_file != "__init__.py":
                    await bot.load_extension(f"cmds.{cog_file.name[:-3]}")

        # for loading slash commands
        if bot_setup.load_onReady_slash:
            for cog_file in settings.SLASH_DIR.glob("*.py"):
                if cog_file != "__init__.py":
                    await bot.load_extension(f"slashcmds.{cog_file.name[:-3]}")

        # for loading cogs
        if bot_setup.load_onReady_cogs:
            for cog_file in settings.COGS_DIR.glob("*.py"):
                if cog_file != "__init__.py":
                    await bot.load_extension(f"cogs.{cog_file.name[:-3]}")


        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)

        async def viewLogs():
            # TODO: View commands within loaded extensions
            print("Commands within loaded extensions (cogs):")
            for cog_name, cog in bot.cogs.items():
                print(f"Cog: {cog_name}")
                for command_name, command in cog.get_commands():
                    print(f"  Command: {command_name}")

            # View loaded SlashCommands
            cms = await bot.tree.fetch_commands(guild=settings.GUILD_ID)
            print(cms)


    @bot.event
    async def on_message(message):  
        if message.author!=bot.user:
            found_word = utilities.count_word(message, bot_setup.count_list)
            if not found_word is None: updateMessage(found_word)
            if utilities.swear_word(message):
                print("we got a swear word!!")
                # TODO: swear words response
            elif message.content.startswith(bot_setup.bot_prefix + "tortle"):
                # PARSE COMMANDS
                await message.delete()
                msg_list = message.content.split()[1:]
                random.shuffle(msg_list)
                msg = ' '.join(msg_list)
                await message.channel.send(msg)
            else:
                await bot.process_commands(message)
        else:
            await bot.process_commands(message)

    # COMMANDS TESTING +++++++++++++++++++++

    # @bot.tree.command()
    # async def 

    # ++++++++++++++++++++++++++++++++++++++


    # ++++++++++++++++++ LOADING AND UNLOADING OF COGS ++++++++++++++++++++
    # @commands.is_owner()
    # @bot.command()
    # async def reload(ctx, cog: str):
    #     await bot.reload_extension(f"cogs.{cog.lower()}")
    #     await ctx.channel.send(f"extension **{cog.lower()}** reloaded")
    
    # @commands.is_owner()
    # @bot.command()
    # async def unload(ctx, cog: str):
    #     await bot.unload_extension(f"cogs.{cog.lower()}")
    #     await ctx.channel.send(f"extension **{cog.lower()}** unloaded")

    # @commands.is_owner()
    # @bot.command()
    # async def load(ctx, cog: str):
    #     await bot.load_extension(f"cogs.{cog.lower()}")
    #     await ctx.channel.send(f"extension **{cog.lower()}** loaded")

    # # @say.error
    # # async def say_error(ctx, error):
    #     if isinstance(error, commands.CommandError):
    #         await ctx.send("Permission denied!!!")
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()