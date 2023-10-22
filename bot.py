import discord
import settings
import random
import json
import utilities
import bot_setup

from discord.ext import commands
from API_requests import requestHandler
from customUI import MyButtonView, MySelectView
from scraper import wikiScraper
from fonts import MyFont
from embed_manager import ListEmbed, TableEmbed
from database_test import fetchData, addFont, updateMessage, fetchSudoku
from bot_prepare import initialize
from sudoku import Sudoku

################## GLOBAL VARIABLES ##########################

logger = settings.logging.getLogger("bot") 
token = settings.DISCORD_API_SECRET

#################################### BOT SETUP ##############################################

bot = commands.Bot(command_prefix=bot_setup.bot_prefix, description=bot_setup.bot_description, intents=bot_setup.getIntents())


@bot.event
async def setup_hook():
    # Perform actions after the bot is logged in
    initialize()
    def fetchChannel(channelID): return bot.get_channel(channelID) or bot.fetch_channel(channelID)
    global messageCountChannel
    global savedMessageChannel
    messageCountChannel = await fetchChannel(bot_setup.messageCountChannelID)
    savedMessageChannel = await fetchChannel(bot_setup.savedMessageChannelID)
    




@bot.event
async def on_ready():
    logger.info(f"Logged on as User: {bot.user} (ID: {bot.user.id})")
    await bot.tree.sync()


######################### BOT COMMANDS AND FUNCTIONS ##################################################

@bot.hybrid_command(name='ping')
async def ping(ctx):
    await ctx.send("pong 👀🧃 ") 


@bot.command(name='button')
async def button(ctx):
    view = MyButtonView(ctx)
    await ctx.send('Hi', view=view)
    await view.wait()

# NON WORKING FUNCTION, MIGHT FIX LATER
@bot.command(name='selection')
async def selection(ctx):
    view = MySelectView(ctx)
    await ctx.send(view=view)


@bot.command(name='viewSaved')
async def viewSaved(ctx):
    count_channel = messageCountChannel
    rows = fetchData()
    embed = discord.Embed(title="Saved Messages", color = 0xfcba03)

    if rows:
        for row in rows:
            embed.add_field(name=row[0], value=f'Count: {row[1]}', inline=False)
    else:
        embed.add_field(name="No data", value="No message counts found.", inline=False)

    await count_channel.send(embed=embed)


@bot.command(name='font')
async def font(ctx, option, *args):
    content = ' '.join(args)
    foption = (option.lower()).strip()

    if(foption in MyFont.font_names()):
        font_name = option
        await ctx.message.delete()
        newMsg = MyFont.translator(content, font_name=font_name)
        await ctx.send(newMsg)
        return
    
    if(foption == 'help'):
        dictt = {
            f"{bot_setup.bot_prefix}font <font_name> <message>" : "Convert your text into a font-styled message",
            f"{bot_setup.bot_prefix}font fonts" : "Displays available fonts",
            f"{bot_setup.bot_prefix}font add <new_font_name> <abcdefghijklmnoprstuwvxyz>" : "Adds new font with the name <new_font_name>. Make sure to put your font letters in the exact order as specified in this help message"
        }
        embed = ListEmbed(ctx, "Fonts Help Page 🇦 🈂️ 🈺", dictt)
        await ctx.send(embed=embed)
        return
    
    if(foption == 'fonts'):
        newstr = "\n".join(MyFont.fancy_font_names())
        embed=discord.Embed(title="Available Fonts:", description=newstr)
        await ctx.send(embed=embed)
        return

    if(foption == 'add'):
        if (len(args) == 2):
            if not args[0]:
                await ctx.send("No font name specified you idiot")
                return
            if not args[1]:
                await ctx.send("Prove the alphabet you dum dum!")
                return
            if (len(args[1])!=len("abcdefghijklmnoprstuwvxyz")):
                await ctx.send(f"Wrong alphabet size. Please see the command {bot_setup.bot_prefix}font help")
                return
            fontName = args[0] 
            alphabet = args[1]
            message = MyFont.add_local_font(addFont(font_name=fontName, alphabet=alphabet))
        else:
            await ctx.send(f"Wrong use of {bot_setup.bot_prefix}font add. See command {bot_setup.bot_prefix}font help")


@bot.command(name='save')
async def save(ctx):
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    saved_channel = savedMessageChannel
    usr = ctx.message.reference.resolved.author
    embed=discord.Embed(title="", description=message.content, color=usr.accent_color)
    embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
    await saved_channel.send(embed=embed)


@bot.command(name='sudoku')
async def sudoku(ctx, size=3, difficulty=75):
    size = int(size)
    difficulty = int(difficulty)
    size = utilities.clamp(size, 2, 10)
    sdk = Sudoku(size, difficulty)

    stringer = sdk.prettyPrint()
    newstr = "```\n"+stringer+"\n```"
    embed=discord.Embed(title=f"Sudoku size: {sdk.side}x{sdk.side} Difficulty: {sdk.difficulty}", description=newstr, color=0x42f56f)
    await ctx.send(embed=embed)


@bot.command(name='sudokus')
async def sudokus(ctx):
    count_channel = messageCountChannel
    # generate dict for ListEmbed:
    dicto = {}
    if len(Sudoku.sudoku_list) == 0:
        await count_channel.send("There are no saved sudoku baords :sadcute:")
        return
    i = 1
    for sdk in Sudoku.sudoku_list:
        if sdk:
            newstr = "```\n"+sdk.prettyPrint()+"\n```"
            line_name = f"{i}) Sudoku size: {sdk.side}x{sdk.side} Difficulty: {sdk.difficulty}"
            dicto.update({line_name : newstr})
            i = i+1
        else:
            pass
    
    embed = ListEmbed(ctx, "Saved Sudoku Boards", dicto, color = 0xffd152)
    if len(dicto) != 0:
        await count_channel.send(embed=embed)
    else:
        await count_channel.send("There are no saved sudoku baords")

class insertFlags(commands.FlagConverter):
    group: int = commands.flag(description='The group number (1-9)')
    square: int = commands.flag(description='The square number (1-9)')
    num: int = commands.flag(description='The number you want to place')
    sdk_choice: int = commands.flag(default=0, description='Which sudoku? Default is last modified')


@bot.hybrid_command(name='insert')
async def insert(ctx, *, flags: insertFlags):
    flags.sdk_choice = utilities.clamp(flags.sdk_choice, 0, len(Sudoku.sudoku_list))
    flags.sdk_choice = flags.sdk_choice - 1
    try:
        # TODO: create a way to choose which sudoku u want to edit
        sdk = Sudoku.sudoku_list[flags.sdk_choice] 
        sdk.inputNum(flags.group,flags.square,flags.num)

        stringer = sdk.prettyPrint()
        newstr = "```\n"+stringer+"\n```"
        embed=discord.Embed(title=f"Sudoku size: {sdk.side}x{sdk.side} Difficulty: {sdk.difficulty}", description=newstr, color=0x42f56f)
        await ctx.send(embed=embed)
    except IndexError as err:
        await ctx.send(err)

@bot.command(name='wiki')
async def wiki(ctx, *args):
    query = ' '.join(args)
    results = wikiScraper.wikiSearches(query)
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


@bot.command(name='chemicals')
async def chemicals(ctx, *args):
    chem_list_to_display = wikiScraper.chemicalsSearchResults(chemicals_list=args)
    usr = ctx.message.author
    for chemical in chem_list_to_display:
        embed=discord.Embed(title=chemical.query, description=chemical.content, color=usr.accent_color)
        await ctx.send(embed=embed)


@bot.command(name='chem')
async def chem(ctx, *args):
    chem_list_to_display = wikiScraper.wikiSearchResults(args, bot_setup.chem_attributes_list)
    usr = ctx.message.author
    for chemical in chem_list_to_display:
        embed=discord.Embed(title=chemical.query, description=chemical.content, color=usr.accent_color, url=chemical.url)
        await ctx.send(embed=embed)


@bot.command(name='toggle')
async def toggle(ctx, setting, *args):
    a=3
    # TODO: toggle functon to change bot settings on/off
    

@bot.command(name='chemData')   
async def chemData(ctx, *args):
    chem_list_to_display = wikiScraper.combinedSearchResults(
        chemicals_list=args, interested_list=bot_setup.chem_attributes_list
        )
    usr = ctx.message.author
    field_embed = True

    for chemical in chem_list_to_display:
        if(field_embed):
            dictt = chemical.result_dict
            embed=discord.Embed(title=chemical.query, description="", color=usr.accent_color, url=chemical.url)
            for key, value in dictt.items():
                embed.add_field(name=key, value=value, inline=False)
        else:
            embed=discord.Embed(title=chemical.query, description=chemical.content, color=usr.accent_color, url=chemical.url)
        await ctx.send(embed=embed)


@bot.command(name='wolfram')
async def wolfram(ctx, *args):
    query = '+'.join(args)
    response = requestHandler(query).API_getWolfram()
    usr = ctx.message.author
    
    if response.status_code == 501:
        await ctx.send("That's some gibberish right there 👀🧃")
        return
    try:
        text_response = json.loads(response.text)["result"]
        question = ' '.join(args)
        embed=discord.Embed(title=question, description=text_response, color=usr.accent_color)
        embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
        await ctx.send(embed=embed)
    except KeyError:
        await ctx.send("That's some gibberish right there 👀🧃\nYou gotta be more precise next time 😊")
        

@bot.command(pass_context = True, name='clear')
async def clear(ctx, number=1):
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    number = utilities.clamp(number, 1, 6)

    channel = ctx.message.channel
    async for message in channel.history(limit = number):
        mgs.append(message)
    for message in mgs:
        await message.delete()

@bot.event
async def on_message(message):
    if message.author!=bot.user:
        found_word = utilities.count_word(message, bot_setup.count_list)
        if not found_word is None: updateMessage(found_word)
        if utilities.swear_word(message):
            print("we got a swear word!!")
            # TODO: swear words response
        elif message.content.startswith(bot_setup.bot_prefix + "tortle"):
            await message.delete()
            msg_list = message.content.split()[1:]
            random.shuffle(msg_list)
            msg = ' '.join(msg_list)
            await message.channel.send(msg)
        else:
            await bot.process_commands(message)
    else:
        await bot.process_commands(message)

################# RUNNING THE BOT #####################################

bot.run(token, root_logger=True)

######################################################################