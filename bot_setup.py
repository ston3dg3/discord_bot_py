# File for setting server-specific bot variables
# TODO: set these variables through bot commands from discord

from typing import Any
from discord import Intents
from utilities import tryDict
import json
from envReplacement import working_path


with open(working_path+"/bot_settings.json") as json_file:
    data = json.load(json_file)

    global messageCountChannelID
    global savedMessageChannelID
    channelID = tryDict(data, "channelID")
    messageCountChannelID = tryDict(channelID, "messageCountChannelID")
    savedMessageChannelID = tryDict(channelID, "savedMessageChannelID")

    global bot_prefix
    global bot_description
    botParams = tryDict(data, "botParams")
    bot_prefix = tryDict(botParams, "bot_prefix")
    bot_description = tryDict(botParams, "bot_description")

    global swear_words
    global count_list
    global chem_attributes_list
    lists = tryDict(data, "lists")
    swear_words = tryDict(lists, "swear_words")
    count_list = tryDict(lists, "count_list")
    chem_attributes_list = tryDict(lists, "chem_attributes_list")

    global swear_notice1
    global swear_notice2
    longStrings = tryDict(data, "longStrings")
    swear_notice1 = tryDict(longStrings, "swear_notice1")
    swear_notice2 = tryDict(longStrings, "swear_notice2")

def getIntents():
    bot_intents = Intents.default()
    bot_intents.members = True
    bot_intents.message_content = True
    return bot_intents


############## OLD VARIABLES #####################

# localFontDict = {
#     "gothic":"𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖗𝖘𝖙𝖚𝖜𝖛𝖝𝖞𝖟",
#     "wide":"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｒｓｔｕｗｖｘｙｚ",
#     "bold":"𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐫𝐬𝐭𝐮𝐰𝐯𝐱𝐲𝐳",
#     "tiny":"ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘʀꜱᴛᴜᴡᴠxʏᴢ"
# }

    