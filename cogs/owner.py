import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return commands.is_owner()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Owner Cog is ready.')

    @commands.command(name='shutdown', help='This command shuts down the bot.')
    async def shutdown(self, ctx):
        await ctx.send('Shutting down...')
        await ctx.bot.close()


async def setup(bot):
    await bot.add_cog(Owner(bot))
