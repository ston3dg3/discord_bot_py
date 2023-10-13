# Easily manage embeds
from discord import Embed
import random


random_colour = f"#{random.randrange(0x1000000):06x}"


def ListEmbed(ctx, title: str, value_desc_dict: dict, author_info = False, url = None, color=0xc592e5) -> Embed:
    embed = Embed(title=title, description="", color=color)
    usr = ctx.message.author
    
    a = (len(value_desc_dict))
    print(f"dict length: {a}")
    for key, value in value_desc_dict.items():
        print(key+ " " + value)
        embed.add_field(name=key, value=value, inline=False)
        if author_info:
            embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)

    return embed


def TableEmbed():
    pass
    # TODO: implement Table embed


