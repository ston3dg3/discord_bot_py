from customUI import MySelectView, getSelectOptions
import scraper
import json
from API_requests import requestHandler
import bot_setup
from embed_manager import EmptyEmbed
import scraper

# returns the closest wiki searches and lets user choose the most accurate
# then displays the summary of the article for the chosen topic
async def wiki(query, channel):
    results = scraper.wikiScraper.wikiSearches(query)
    if not results:
        return "What are you on about u dummy? 😤"
    else:
        embed = SelectViewSender(channel=channel, options=results)
        return embed

# use *args: commands.Greedy[str] to get many arguments
def chem(chemicals, usr):
    chem_list_to_display = scraper.wikiScraper.wikiSearchResults(chemicals, bot_setup.chem_attributes_list)
    embed_list = []
    for chemical in chem_list_to_display:
        embed=EmptyEmbed(title=chemical.query, description=chemical.content, color=usr.accent_color, url=chemical.url)
        embed_list.apped(embed)
    return embed_list


# returns an answer from the Wolfram API given user input question
def wolfram(question, usr):
    query = '+'.join(question)
    response = requestHandler(query).API_getWolfram()
    if response.status_code == 501:
        return"That's some gibberish right there 👀🧃"
    try:
        text_response = json.loads(response.text)["result"]
        embed=EmptyEmbed(title=question, description=text_response, color=usr.accent_color)
        embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
        return embed
    except KeyError:
        return "That's some gibberish right there 👀🧃\nYou gotta be more precise next time 😊"
    

async def SelectViewSender(channel, options):
    view = MySelectView(channel).add_select_options(options=getSelectOptions(options))
    await channel.send(view=view)
    await view.wait()
    embed = EmptyEmbed(title=view.sel_opt, description=view.summary, color=0xff33cc)
    view.clear_items()
    return embed
