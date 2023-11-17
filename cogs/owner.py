import discord
from discord.ext import commands


class Owner(commands.Cog, description='This is a cog for the owner commands.'):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return commands.is_owner()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Owner Cog is ready.')

    @commands.command(name='shutdown', help='This command shuts down the bot.')
    async def shutdown(self, ctx):
        await ctx.send(embed=discord.Embed(title='Shutting down...', color=discord.Color.red()))
        await ctx.bot.close()

    @commands.command(name='cogs', help='This command lists all of the cogs. It has no arguments', aliases=['cog'], brief='This command lists all of the cogs.', description='This command lists all of the cogs.')
    async def cogs(self, ctx):
        list_cogs = [self.bot.cogs[cog].qualified_name for cog in self.bot.cogs]
        list_descriptions = [self.bot.cogs[cog].description for cog in self.bot.cogs]
        list_cogs = [f'**{list_cogs[i]}** - {list_descriptions[i]}' for i in range(len(list_cogs))]
        list_cogs = '\n'.join(list_cogs)
        embed = discord.Embed(title='List Of Cogs', description=list_cogs, color=discord.Color.green())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Owner(bot))
