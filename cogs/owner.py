import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(selfs):
        print('Owner Cog is ready.')

    # @Client.command(name='Shutdown', help='This command shuts down the bot.')
    # async def shutdown(self, ctx):
     #   await ctx.send('Shutting down...')
      #  await ctx.bot.logout()


async def setup(bot):
    await bot.add_cog(Owner(bot))