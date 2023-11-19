import discord
from discord import app_commands

# here specify the main command as name
async def setup(bot):
    grp = MyGroup(name="puffer", description="says priinces puffer")
    bot.tree.add_command(grp)


class MyGroup(app_commands.Group):

    @app_commands.command()
    async def print(self, interaction: discord.Interaction):
        await interaction.response.send_message("princcess puffer")
