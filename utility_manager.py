from embed_manager import EmptyEmbed, ListEmbed
from database_test import fetchData
import utilities

# save a message to the saved_messages channel
async def save(messageToSave, usr, saved_channel):
    embed=EmptyEmbed(title="", description=messageToSave.content, color=usr.accent_color)
    embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
    await saved_channel.send(embed=embed)

# view all saved messages and their counts
async def viewSaved(display_channel):
    rows = fetchData()
    dictt = None
    if rows:
        dictt = {str(row[0]):str(row[1]) for row in rows}
        embed = ListEmbed("Saved Messages", dictt, color=0xfcba03)
        await display_channel.send(embed=embed)
    else:
        # return an Embed with a field containing the error message
        embed = EmptyEmbed("Saved Messages", "No message counts found!", utilities.randomColour())
        await display_channel.send(embed=embed)
    
# delete number of messages
async def clear(number, delete_channel):
    mgs = [] #Empty list to put all the messages in the log
    number = utilities.clamp(int(number), 1, 6)

    async for message in delete_channel.history(limit = number):
        mgs.append(message)
    for message in mgs:
        await message.delete()