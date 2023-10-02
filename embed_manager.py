# Easily manage embeds
from discord import Embed
import random


random_colour = f"#{random.randrange(0x1000000):06x}"


def ListEmbed(ctx, title: str, value_desc_dict: dict, author_info = False, url = None) -> Embed:
    embed = Embed(title=title, description="", color=0xc592e5)
    usr = ctx.message.author
    
    for key, value in value_desc_dict.items():
        embed.add_field(name=key, value=value, inline=False)
        if author_info:
            embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)


def TableEmbed():
    pass
    # TODO: implement Table embed


