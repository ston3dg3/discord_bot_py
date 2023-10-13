# File for setting server-specific bot variables
# TODO: set these variables through bot commands from discord

from typing import Any
from discord import Intents
from utilities import tryDict
import json

with open('bot_settings.json') as json_file:
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

class bot_parameters:

    @classmethod
    def getIntents(self):
        bot_intents = Intents.default()
        bot_intents.members = True
        bot_intents.message_content = True
        return bot_intents
    
    

    messageCountChannelID = 1152392328699461682
    
    savedMessageChannelID = 1152273521028898856

    bot_prefix = "$"

    bot_description = "Michiyo is a pufferfish"

    swear_words = [
        "asian", "white", "black", "nigger", "nigga", "racist"
    ]

    count_list = [
        "bb", "cow", "asian", "white", "tortle", "neko", "racist",
        "tummy", "pee"
    ]
    
    swear_notice1 = "Hi Franek dont be racist bc michiyo will get mad at u"

    swear_notice2 = """
        Dear Discord User,
        I hope this message finds you well. We appreciate your presence on our Discord server and value your contributions to our community. However, we've noticed that there have been instances of swearing in your recent messages.
        Our server is committed to providing a welcoming and respectful environment for all members, and as such, we have a policy against the use of explicit language. We kindly request that you refrain from swearing in the future to maintain the positive atmosphere we strive to create.
        We understand that slips can happen, but repeated violations may lead to more serious actions, such as a temporary mute or, in extreme cases, removal from the server. We sincerely hope it doesn't come to that and would prefer to continue enjoying your presence here.
        If you have any questions or concerns regarding our server rules or any other matter, please feel free to reach out to one of our moderators or administrators. They are always ready to assist you.
        Thank you for your understanding and cooperation in this matter. Let's work together to keep our server a pleasant place for everyone.
        Best regards,
        Server Administration (and Tortle)
                    """
    
    chem_attributes_list = [
        'Chemical formula', 'Molar mass', 'Appearance', 'Density', 
        'Melting point', 'Boiling point', 'Solubility', 'Solubility in water'
    ]


############## OLD VARIABLES #####################

# localFontDict = {
#     "gothic":"𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖗𝖘𝖙𝖚𝖜𝖛𝖝𝖞𝖟",
#     "wide":"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｒｓｔｕｗｖｘｙｚ",
#     "bold":"𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐫𝐬𝐭𝐮𝐰𝐯𝐱𝐲𝐳",
#     "tiny":"ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘʀꜱᴛᴜᴡᴠxʏᴢ"
# }

    