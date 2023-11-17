import discord
from discord.ext import commands


class Ping(commands.Cog, description='This is a cog for the ping command.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):  # This event is called when the bot is ready
        print('Ping is ready.')

    @commands.command(name='ping', brief='This command returns the latency', help='This command gives the latency. It has no arguments.')
    async def ping(self, ctx):
        await ctx.send(f'**Pong!** Latency: {round(self.bot.latency * 1000)}ms')


async def setup(bot):
    await bot.add_cog(Ping(bot))
