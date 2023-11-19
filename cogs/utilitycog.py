from discord.ext import commands
import bot_setup
import utility_manager

async def setup(bot):
    if (bot_setup.load_ext):
        await bot.add_cog(UtilityCog(bot))

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='save')
    async def save(self, ctx):
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        saved_channel = bot_setup.savedMessageChannel
        user = ctx.message.reference.resolved.author
        await utility_manager.save(message, user, saved_channel)

    @commands.command(name='viewSaved')
    async def viewSaved(self, ctx):
        display_channel = bot_setup.messageCountChannel
        await utility_manager.viewSaved(display_channel)

    @commands.command(pass_context = True, name='clear')
    async def clear(self, ctx, number=1):
        deleteChannel = ctx.message.channel
        await utility_manager.clear(number, deleteChannel)
   