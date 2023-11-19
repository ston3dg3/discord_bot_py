# from fonts import MyFont
# import discord
# from discord.ext import commands
# from embed_manager import ListEmbed
# import utilities
# from sudoku import Sudoku
# from ANSI_colours import ANSI
# import bot_setup
# from scraper import wikiScraper
# import json
# from customUI import MyButtonView, MySelectView
# import settings

# @bot.event
# async def on_ready():
#     for cmd_file in settings.CMDS_DIR.glob("*.py"):
#         if cmd_file.name != "__init__.py":
#             await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")


# @bot.command(name='font')
# async def font(ctx, option, *args):
#     content = ' '.join(args)
#     foption = (option.lower()).strip()

#     if(foption in MyFont.font_names()):
#         font_name = option
#         await ctx.message.delete()
#         newMsg = MyFont.translator(content, font_name=font_name)
#         await ctx.send(newMsg)
#         return
    
#     if(foption == 'help'):
#         dictt = {
#             "/font <font_name> <message>" : "Convert your text into a font-styled message",
#             "/font fonts" : "Displays available fonts",
#             "/font add <new_font_name> <abcdefghijklmnoprstuwvxyz>" : "Adds new font with the name <new_font_name>. Make sure to put your font letters in the exact order as specified in this help message"
#         }
#         embed = ListEmbed(ctx, "Fonts Help Page 🇦 🈂️ 🈺", dictt)
#         await ctx.send(embed=embed)
#         return
    
#     if(foption == 'fonts'):
#         newstr = "\n".join(MyFont.fancy_font_names())
#         embed=discord.Embed(title="Available Fonts:", description=newstr)
#         await ctx.send(embed=embed)
#         return

#     if(foption == 'add'):
#         if (len(args) == 2):
#             if not args[0]:
#                 await ctx.send("No font name specified you idiot")
#                 return
#             if not args[1]:
#                 await ctx.send("Prove the alphabet you dum dum!")
#                 return
#             if (len(args[1])!=len("abcdefghijklmnoprstuwvxyz")):
#                 await ctx.send("Wrong alphabet size. Please see the command /font help")
#                 return
#             fontName = args[0] 
#             alphabet = args[1]
#             message = MyFont.add_local_font(addFont(font_name=fontName, alphabet=alphabet))
#         else:
#             await ctx.send("Wrong use of /font add. See command /font help")


# @bot.command(name='save')
# async def save(ctx):
#     message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
#     saved_channel = savedMessageChannel
#     usr = ctx.message.reference.resolved.author
#     embed=discord.Embed(title="", description=message.content, color=usr.accent_color)
#     embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
#     await saved_channel.send(embed=embed)


# class sudokuFlags(commands.FlagConverter):
#     option: str = commands.flag(description="What do you want to do? [new] - Create new Sudoku. [save] - Save current sudoku. [list] - List all sudoku boards")
#     difficulty: int = commands.flag(description="Easiest: [10], Hardest: [80]. Default 70", default=70)
#     size: int = commands.flag(description="Sudoku size. Range [2-10]. Default 3", default=3)

# @bot.hybrid_command(name='sudoku')
# async def sudoku(ctx, *, flags: sudokuFlags):

#     sudoku_channel = messageCountChannel

#     if (flags.option == "new"):
#         await ctx.send(embed = createSudoku())
#     elif (flags.option == "save"):
#         await ctx.send(saveSudoku())
#     elif (flags.option == "list"):
#         lst = listSudokus()
#         if (type(lst) == type("string")):
#             await ctx.send(lst)
#         else:
#             await sudoku_channel.send(embed=lst)
#     else:
#         await ctx.send("Invalid option. Choose one of: [new] [save] [list]")

#     def createSudoku():
#         size = utilities.clamp(flags.size, 2, 10)
#         difficulty = utilities.clamp(flags.difficulty, 10,80)
#         sdk = Sudoku(size, difficulty)
#         newstr = ANSI.wrapANSIblock(sdk.prettyPrint())
#         embed=discord.Embed(title=f"Sudoku size: {sdk.side}x{sdk.side} Difficulty: {sdk.difficulty}", description=newstr, color=0x42f56f)
#         return embed
    
#     def listSudokus():
#         # generate dict for ListEmbed:
#         dicto = {}
#         if len(Sudoku.sudoku_list) == 0:
#             return "There are no saved sudoku baords :("
#         i = 1
#         for sdk in Sudoku.sudoku_list:
#             if sdk:
#                 newstr = ANSI.wrapANSIblock(sdk.prettyPrint())
#                 line_name = f"{i}) Sudoku size: {sdk.side}x{sdk.side} Difficulty: {sdk.difficulty}"
#                 dicto.update({line_name : newstr})
#                 i = i+1
#             else:
#                 # SUDOKU is None
#                 pass

#         embed = ListEmbed(ctx, "Saved Sudoku Boards", dicto, color = 0xffd152)
#         if len(dicto) != 0:
#             return embed
#         else:
#             return "There are no saved sudoku baords :("

#     def saveSudoku():
#         sdk = Sudoku.sudoku_list[-1]
#         sdk.store()
#         return f"Successfully saved Sudoku with ID: <{sdk.key}>\nView it with: /sudoku list"
        

# class insertFlags(commands.FlagConverter):
#     group: int = commands.flag(description='The group number (1-9)')
#     square: int = commands.flag(description='The square number (1-9)')
#     num: int = commands.flag(description='The number you want to place')
#     sdk_choice: int = commands.flag(default=0, description='Which sudoku? Default is last modified')


# @bot.hybrid_command(name='insert')
# async def insert(ctx, *, flags: insertFlags):
#     flags.sdk_choice = utilities.clamp(flags.sdk_choice, 0, len(Sudoku.sudoku_list))
#     flags.sdk_choice = flags.sdk_choice - 1
#     try:
#         # TODO: create a way to choose which sudoku u want to edit
#         sdk = Sudoku.sudoku_list[flags.sdk_choice] 
#         sdk.inputNum(flags.group,flags.square,flags.num)

#         stringer = sdk.prettyPrint()
#         newstr = "```\n"+stringer+"\n```"
#         embed=discord.Embed(title=f"Sudoku size: {sdk.side}x{sdk.side} Difficulty: {sdk.difficulty}", description=newstr, color=0x42f56f)
#         await ctx.send(embed=embed)
#     except IndexError as err:
#         await ctx.send(err)

# class wikiFlags(commands.FlagConverter):
#     search_term: str = commands.flag(description="Insert a topic that you want to search on Wikipedia")

# @bot.hybrid_command(name='wiki')
# async def wiki(ctx, *, flags: wikiFlags):
#     query = flags.search_term
#     results = wikiScraper.wikiSearches(query)
#     if not results:
#             await ctx.send("What are you on about u dummy? 😤")
#             return
#     results = [discord.SelectOption(label=result, value=result) for result in results]
#     view = MySelectView(ctx)
#     view.add_select_options(options=results)
#     await ctx.send(view=view)
#     await view.wait()
#     embed=discord.Embed(title=view.sel_opt, description=view.summary, color=0xff33cc)
#     await ctx.send(embed=embed)
#     view.clear_items()


# # DEPRECIATED TODO: Exorcise command
# # @bot.command(name='chemicals')
# # async def chemicals(ctx, *args):
# #     chem_list_to_display = wikiScraper.chemicalsSearchResults(chemicals_list=args)
# #     usr = ctx.message.author
# #     for chemical in chem_list_to_display:
# #         embed=discord.Embed(title=chemical.query, description=chemical.content, color=usr.accent_color)
# #         await ctx.send(embed=embed)


# @bot.hybrid_command(name='chem')
# async def chem(ctx, *args: commands.Greedy[str]):
#     chem_list_to_display = wikiScraper.wikiSearchResults(args, bot_setup.chem_attributes_list)
#     usr = ctx.message.author
#     for chemical in chem_list_to_display:
#         embed=discord.Embed(title=chemical.query, description=chemical.content, color=usr.accent_color, url=chemical.url)
#         await ctx.send(embed=embed)


# @bot.command(name='toggle')
# async def toggle(ctx, setting, *args):
#     a=3
#     # TODO: toggle functon to change bot settings on/off
    
# # TODO: Needs to work without chemicals library
# # @bot.command(name='chemData')   
# # async def chemData(ctx, *args):
# #     chem_list_to_display = wikiScraper.combinedSearchResults(
# #         chemicals_list=args, interested_list=bot_setup.chem_attributes_list
# #         )
# #     usr = ctx.message.author
# #     field_embed = True

# #     for chemical in chem_list_to_display:
# #         if(field_embed):
# #             dictt = chemical.result_dict
# #             embed=discord.Embed(title=chemical.query, description="", color=usr.accent_color, url=chemical.url)
# #             for key, value in dictt.items():
# #                 embed.add_field(name=key, value=value, inline=False)
# #         else:
# #             embed=discord.Embed(title=chemical.query, description=chemical.content, color=usr.accent_color, url=chemical.url)
# #         await ctx.send(embed=embed)

# class wolframFlags(commands.FlagConverter):
#     search_term: str = commands.flag(description="Insert a question for the Wolfram engine")


# @bot.hybrid_command(name='wolfram')
# async def wolfram(ctx, question: wolframFlags):
#     query = '+'.join(question)
#     response = requestHandler(query).API_getWolfram()
#     usr = ctx.message.author
    
#     if response.status_code == 501:
#         await ctx.send("That's some gibberish right there 👀🧃")
#         return
#     try:
#         text_response = json.loads(response.text)["result"]
#         question = ' '.join(question)
#         embed=discord.Embed(title=question, description=text_response, color=usr.accent_color)
#         embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
#         await ctx.send(embed=embed)
#     except KeyError:
#         await ctx.send("That's some gibberish right there 👀🧃\nYou gotta be more precise next time 😊")
        

# @bot.command(pass_context = True, name='clear')
# async def clear(ctx, number=1):
#     mgs = [] #Empty list to put all the messages in the log
#     number = int(number) #Converting the amount of messages to delete to an integer
#     number = utilities.clamp(number, 1, 6)

#     channel = ctx.message.channel
#     async for message in channel.history(limit = number):
#         mgs.append(message)
#     for message in mgs:
#         await message.delete()