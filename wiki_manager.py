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
        await channel.send("What are you on about u dummy? 😤")
        return
    options = getSelectOptions(results)
    view = MySelectView(channel)
    view.add_select_options(options=options)
    await channel.send(view=view)
    await view.wait()
    embed=EmptyEmbed(title=view.sel_opt, description=view.summary, color=0xff33cc)
    await channel.send(embed=embed)
    view.clear_items()


# use *args: commands.Greedy[str] to get many arguments
async def chem(chemicals, channel, usr):
    chem_list_to_display = scraper.wikiScraper.wikiSearchResults(chemicals, bot_setup.chem_attributes_list)
    for chemical in chem_list_to_display:
        embed=EmptyEmbed(title=chemical.query, description=chemical.content, color=usr.accent_color, url=chemical.url)
        await channel.send(embed=embed)


# returns an answer from the Wolfram API given user input question
async def wolfram(question, channel, usr):
    query = '+'.join(question)
    response = requestHandler(query).API_getWolfram()
    if response.status_code == 501:
        await channel.send("That's some gibberish right there 👀🧃")
        return
    try:
        text_response = json.loads(response.text)["result"]
        embed=EmptyEmbed(title=question, description=text_response, color=usr.accent_color)
        embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
        await channel.send(embed=embed)
    except KeyError:
        await channel.send("That's some gibberish right there 👀🧃\nYou gotta be more precise next time 😊")
