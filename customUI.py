from discord.interactions import Interaction
from discord.ui import View, Button, Select, button, select
from discord.ui.item import Item
from scraper import wikiScraper
from discord import ButtonStyle
from discord import SelectOption


# File with custom UI classes, mainly subclassing discord.View


class MyButtonView(View):

    def __init__(self, ctx):
        super().__init__(timeout=3)
        self.ctx = ctx
        self.value = None

    @button(label = 'press me', emoji='😊', style=ButtonStyle.green, custom_id="green")
    async def green_button_callback(self, interaction, button):
        button_red = [x for x in self.children if x.custom_id=="red"][0]
        button.label = "good job"
        button.disabled = True
        button_red.disabled = True
        self.value = "green"
        await interaction.response.edit_message(view=self)

    @button(label = 'dont press on me', emoji='😕', style=ButtonStyle.red, custom_id="red")
    async def red_button_callback(self, interaction, button):
        button_green = [x for x in self.children if x.custom_id=="green"][0]
        button.label = "stop it!"
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

class MySelectView(View):
    def __init__(self, channel):
        super().__init__(timeout=25)
        self.channel = channel
        self.sel_opt = None
        self.summary = None

    # this select is a placeholder, will change
    # parameters dynamically through input from bot.py
    @select(
        custom_id="menuMenu",
        placeholder="Which one u looking for? 👀🧃",
        min_values=1,
        max_values=1,
        options = []
    )
    async def select_callback(self, interaction: Interaction, select: Select):
        selected_option = select.values[0]
        summary = wikiScraper.wikiSummary(selected_option)
        self.sel_opt = selected_option
        self.summary = summary

        select.disabled = True
        self.stop()
        await interaction.response.edit_message(view=self)

    def add_select_options(self, options):
        self.select_callback.options = options

    async def on_timeout(self):
        if not self.is_finished():
            await self.channel.send("You were taking too long sucker! 😝")
            self.clear_items()


####################### FUNCTIONS #########################################

def getSelectOptions(displayOptions: "list[str]"):
    if len(displayOptions)==0 or displayOptions is None:
        # TODO: raise exception
        return None
    options = [SelectOption(label=option, value=option) for option in displayOptions]
    return options