import discord
from discord.ext import commands
import json


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Embed is ready.')

    @commands.command(name="embed")
    async def embed(self, ctx):
        embed = discord.Embed(title='Title', description='Description', colour=discord.Colour.blue())
        embed.set_footer(text='Footer')
        embed.set_image(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Embed(bot))
