import discord
from discord.ext import commands
from discord.ext.commands import bot


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return True if ctx.author.id == 396492370998460420  else False
    @commands.Cog.listener()
    async def on_ready(selfs):
        print('Owner Cog is ready.')

    @commands.command(name='shutdown', help='This command shuts down the bot.')
    async def shutdown(self, ctx):
        await ctx.send('Shutting down...')
        await ctx.bot.close()



async def setup(bot):
    await bot.add_cog(Owner(bot))