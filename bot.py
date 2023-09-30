import os
import settings
from dotenv import load_dotenv
from typing import Any, Coroutine, Optional
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View
import random
import json
import re
from discord.ui.item import Item
import requests
from scraper import wikiScraper
from fonts import MyFont
from database_test import create_fonts_table, updateMessage, fetchData, addFont, create_message_table, requestAllFonts

############### API KEYS ####################################

token = settings.DISCORD_API_SECRET
wolfram_ID = settings.WOLFRAM_API_ID

################## GLOBAL VARIABLES ##########################

logger = settings.logging.getLogger("bot")
description = 'a lazy bot'
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
prefix = "$"
messageCountChannelID = 1152392328699461682

#################################### BOT SETUP ##############################################

bot = commands.Bot(command_prefix=prefix, description="Michiyo is a pufferfish", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Logged on as User: {bot.user} (ID: {bot.user.id})")
    await bot.tree.sync()

    create_fonts_table()
    create_message_table()

    [MyFont.add_local_font(row) for row in requestAllFonts()]
            
############################# CUSTOM CLASSES #########################################################

class MyButtonView(View):

    def __init__(self, ctx):
        super().__init__(timeout=3)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label = 'PRESS ME!', emoji='🥵', style=discord.ButtonStyle.green, custom_id="green")
    async def green_button_callback(self, interaction, button):
        button_red = [x for x in self.children if x.custom_id=="red"][0]
        button.label = "good girl<3"
        button.disabled = True
        button_red.disabled = True
        self.value = "green"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = 'dont press on me', emoji='😖', style=discord.ButtonStyle.red, custom_id="red")
    async def red_button_callback(self, interaction, button):
        button_green = [x for x in self.children if x.custom_id=="green"][0]
        button.label = "STOP IT!"
        button.disabled = True
        button_green.disabled = True
        self.value = "red"
        await interaction.response.edit_message(view=self)

    async def on_timeout(self):
        await self.ctx.send("Timeout!")
        self.clear_items()

    async def on_error(self, interaction, error, item) -> None:
        await interaction.response.send_message(str(error))

##################################################################

class MySelectView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=25)
        self.ctx = ctx
        self.sel_opt = None
        self.summary = None

    @discord.ui.select(
        custom_id="menuMenu",
        placeholder="Which one u looking for? 👀🧃",
        min_values=1,
        max_values=1,
        options = []
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        selected_option = select.values[0]
        summary = wikiScraper.wikiSummary(selected_option)
        self.sel_opt = selected_option
        self.summary = summary

        select.disabled = True
        self.stop()
        self.clear_items()
        await interaction.response.edit_message(view=self)

    def add_select_options(self, options):
        self.select_callback.options = options

    async def on_timeout(self):
        if not self.is_finished():
            await self.ctx.send("You were taking too long sucker! 😝")
            self.clear_items()


######################### BOT COMMANDS AND FUNCTIONS ##################################################

@bot.hybrid_command(name='ping')
async def ping(ctx):
    await ctx.send("pong 👀🧃 ") 

@bot.command(name='button')
async def button(ctx):
    view = MyButtonView(ctx)
    await ctx.send('Hi', view=view)
    await view.wait()

@bot.command(name='selection')
async def selection(ctx):
    view = MySelectView(ctx)
    await ctx.send(view=view)

@bot.command(name='viewSaved')
async def viewSaved(ctx):
    count_channel = bot.get_channel(messageCountChannelID)
    rows = fetchData()

    # Create an empty embed
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
    if((option.lower()).strip() in MyFont.font_names()):
        font_name = option
        await ctx.message.delete()
        newMsg = MyFont.translator(content, font_name=font_name)
        await ctx.send(newMsg)
        return
    if((option.lower()).strip() == 'help'):
        strrr = "Adds new font with the name <new_font_name>. Make sure to put your font letters in the exact order as specified in this help message"
        embed=discord.Embed(title="Fonts Help Page 🇦 🈂️ 🈺", description="", color=0xff6363)
        embed.add_field(name=f"{prefix}font <font_name> <message>", value="Convert your text into a font-styled message", inline=False)
        embed.add_field(name=f"{prefix}font fonts", value="Displays available fonts", inline=False)
        embed.add_field(name=f"{prefix}font add <new_font_name> <abcdefghijklmnoprstuwvxyz>", value=strrr, inline=False)

        await ctx.send(embed=embed)
        return
    if((option.lower()).strip() == 'fonts'):
        for font in MyFont.fonts:
            print(font)
        newstr = ""
        for x in MyFont.fancy_font_names():
            newstr += f"{x}\n"
        print(newstr)
        embed=discord.Embed(title="Available Fonts: 🇦 🈂️ 🈺", description=newstr)
        await ctx.send(embed=embed)
        return
    print((option.lower()).strip())
    print((content.lower()).strip())
    if((option.lower()).strip() == 'add'):
        if (len(args) == 2):
            if not args[0]:
                await ctx.send("No font name specified you idiot")
                return
            if not args[1]:
                await ctx.send("Prove the alphabet you dum dum!")
                return
            if (len(args[1])!=len("abcdefghijklmnoprstuwvxyz")):
                await ctx.send(f"Wrong alphabet size. Please see the command {prefix}font help")
                return
            fontName = args[0] 
            alphabet = args[1]
            message = MyFont.add_local_font(addFont(font_name=fontName, alphabet=alphabet))
            print(message)
                    
            
        else:
            await ctx.send(f"Wrong use of {prefix}font add. See command {prefix}font help")


@bot.command(name='save')
async def save(ctx):
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    saved_channel = bot.get_channel(1152273521028898856)
    
    usr = ctx.message.reference.resolved.author
    embed=discord.Embed(title="", description=message.content, color=usr.accent_color)
    embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)

    await saved_channel.send(embed=embed)
    #await saved_channel.send("""Message Author - {usr}:\n" """.format(usr = ctx.message.reference.resolved.author.global_name) + message.content + """ " """)

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



@bot.command(name='chemicals')
async def chemicals(ctx, *args):
    #await ctx.send("Type in chemicals as command arguments separated by whitespace 👩‍🔬")
    chem_list_to_display = wikiScraper.chemicalsSearchResults(chemicals_list=args)
    usr = ctx.message.author

    for chemical in chem_list_to_display:
        embed=discord.Embed(title=chemical.query, description=chemical.content, color=usr.accent_color)
        await ctx.send(embed=embed)

@bot.command(name='chem')
async def chem(ctx, *args):
    #await ctx.send("Type in chemicals as command arguments separated by whitespace 👩‍🔬")
    # add items for more search results :P

    chem_list_to_display = wikiScraper.wikiSearchResults(args, moja_lista)
    usr = ctx.message.author

    for chemical in chem_list_to_display:
        embed=discord.Embed(title=chemical.query, description=chemical.content, color=usr.accent_color, url=chemical.url)
        await ctx.send(embed=embed)

@bot.command(name='toggle')
async def toggle(ctx, *args):
    a=3
    
@bot.command(name='chemData')   
async def chemData(ctx, *args):
    #await ctx.send("Type in chemicals as command arguments separated by whitespace 👩‍🔬")

    chem_list_to_display = wikiScraper.combinedSearchResults(chemicals_list=args, interested_list=moja_lista)
    
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
    url = f"https://api.wolframalpha.com/v1/conversation.jsp?appid={wolfram_ID}&i={query}%3f"
    response = requests.get(url)
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
async def clear(ctx, number):
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    channel = ctx.message.channel
    async for message in channel.history(limit = number):
        mgs.append(message)
    for message in mgs:
        await message.delete()

@bot.event
async def on_message(message):
    if message.author!=bot.user:
        channel = message.channel
        author = message.author
        count_word(message, count_list)
        if swear_word(message):
            print("we got a swear word!!")
            # if author.id == 477936801504296994:
            #     await channel.send(polite_swear_notice.format(name="Michiyo Nakashima"))
            # else:
            #     await channel.send(swear_notice_franek)
        elif message.content.startswith(prefix + "tortle"):
            #await bot.process_commands(message)
            await message.delete()
            msg_list = message.content.split()[1:]
            random.shuffle(msg_list)
            msg = ' '.join(msg_list)
            await channel.send(msg)
        else:
            await bot.process_commands(message)
    else:
        await bot.process_commands(message)

def add_to_txt(message):
    msg = message.content
    f = open('fav_list.txt', 'a')
    f.write(msg)
    f.write('\n')
    f.close()




################# FUNCTIONS #####################################



swear_words = [
    "asian", "white", "black", "nigger", "nigga", "racist"
]

count_list = ["bb", "cow", "asian", "white", "tortle", "neko", "racist",
              "tummy", "pee"]

def add_word_to_count(new_word):
    count_word = {
        "word": new_word,
        "count": 0
    }
    json_obj = json.dump(count_word, indent=4)
    file = open("word_count.txt", "a")
    file.write(json_obj)
    file.close()

def swear_word(message):
    msg = message.content
    return any(ele in msg for ele in swear_words)

def count_word(message, mess_list):
    # upper matching also indcludes elements within other strings.
    # matching_element = next((element for element in mess_list if element in message.content), None)
    matching_element = next((element for element in mess_list if re.search(rf'\b{element}\b', message.content)), None)
    if matching_element:
        updateMessage(matching_element)


######################################################################################################

swear_notice_franek = "Hi Franek dont be racist bc michiyo will get mad at u"


polite_swear_notice = """

Dear {name},

I hope this message finds you well. We appreciate your presence on our Discord server and value your contributions to our community. However, we've noticed that there have been instances of swearing in your recent messages.

Our server is committed to providing a welcoming and respectful environment for all members, and as such, we have a policy against the use of explicit language. We kindly request that you refrain from swearing in the future to maintain the positive atmosphere we strive to create.

We understand that slips can happen, but repeated violations may lead to more serious actions, such as a temporary mute or, in extreme cases, removal from the server. We sincerely hope it doesn't come to that and would prefer to continue enjoying your presence here.

If you have any questions or concerns regarding our server rules or any other matter, please feel free to reach out to one of our moderators or administrators. They are always ready to assist you.

Thank you for your understanding and cooperation in this matter. Let's work together to keep our server a pleasant place for everyone.

Best regards,

Server Administration (and Tortle)

"""

# localFontDict = {
#     "gothic":"𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖗𝖘𝖙𝖚𝖜𝖛𝖝𝖞𝖟",
#     "wide":"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｒｓｔｕｗｖｘｙｚ",
#     "bold":"𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐫𝐬𝐭𝐮𝐰𝐯𝐱𝐲𝐳",
#     "tiny":"ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘʀꜱᴛᴜᴡᴠxʏᴢ"
# }

moja_lista = [
    'Chemical formula', 'Molar mass', 'Appearance', 'Density', 
    'Melting point', 'Boiling point', 'Solubility', 'Solubility in water'
    ]


#################################################################

bot.run(token, root_logger=True)