import discord
from discord.ext import commands


class Embed(commands.Cog, description='This is a home for all of the embed commands.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="embed", brief="This command sends an embed.",
                      help="This command sends an embed. It has no arguments.")
    async def embed(self, ctx):
        embed = discord.Embed(title='Title', description='Description', colour=discord.Colour.blue())
        embed.set_footer(text='Footer')
        embed.set_image(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Embed(bot))
