# Easily manage embeds
from discord import Embed
import random
from utilities import randomColour

random_colour = f"#{random.randrange(0x1000000):06x}"


# returns a useful list embed from a dictionary
def ListEmbed(title: str, value_desc_dict: dict, author_info = False, url = None, color=0xc592e5, ctx=None) -> Embed:
    embed = Embed(title=title, description="", color=color)
    if author_info:
        usr = ctx.message.author
    else:
        usr = None

    if value_desc_dict is None:
        embed.add_field(name="No Entries Found", value="N/D", inline=False)
        return embed
    
    for key, value in value_desc_dict.items():
        embed.add_field(name=key, value=value, inline=False)

    if author_info:
        embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)

    return embed

# returns an empty embed so that modules do not require discord.py
def EmptyEmbed(title, description, color=0xff6699, url=None):
    return Embed(title=title, description=description, color=color, url=url)

def addErrorMessage(embed: Embed, error_message = "Requested data could not be found"):
    return embed.add_field(name = error_message, value = "")


    

def TableEmbed():
    pass
    # TODO: implement Table embed


