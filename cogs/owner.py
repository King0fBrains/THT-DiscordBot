import logging
import discord
from discord.ext import commands


class Owner(commands.Cog, description='This is a cog for the owner commands.'):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')

    async def cog_check(self, ctx):
        return commands.is_owner()

    @commands.command(name='shutdown', brief='This command shuts down the bot.',
                      help='This command shuts down the bot. It has no arguments.')
    async def shutdown(self, ctx):
        await ctx.send(embed=discord.Embed(title='Shutting down...', color=discord.Color.red()))
        self.logger.info("Bot issued shutdown command. Exiting")
        await ctx.bot.close()

    @commands.command(name='cogs', help='This command lists all of the cogs. It has no arguments', aliases=['cog'],
                      brief='This command lists all of the cogs.', description='This command lists all of the cogs.')
    async def cogs(self, ctx):
        list_cogs = [self.bot.cogs[cog].qualified_name for cog in self.bot.cogs]
        list_descriptions = [self.bot.cogs[cog].description for cog in self.bot.cogs]
        list_cogs = [f'**{list_cogs[i]}** - {list_descriptions[i]}' for i in range(len(list_cogs))]
        list_cogs = '\n'.join(list_cogs)
        embed = discord.Embed(title='List Of Cogs', description=list_cogs, color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name='invite', brief='This command sends the invite link for the bot.',
                      help='This command sends the invite link for the bot. It has no arguments.')
    async def invite(self, ctx):
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=923764425436049478&permissions=8&scope=bot')

    @commands.command()
    async def issues(self, ctx):
        embed1 = discord.Embed(title='Small Issues', description='lock/unlock \ntags?? \ncustom embeds?',
                               color=discord.Color.green())
        embed2 = discord.Embed(title='Big Issues',
                               description='Restart \n'
                                           'Errors \n Welcome Message', color=discord.Color.orange())
        await ctx.send(embeds=[embed1, embed2])

    @commands.command()
    async def reload(self, ctx, cog):
        c = "cogs." + cog
        try:
            await self.bot.reload_extension(c)
            await ctx.send(f"Reloaded extension `{cog}`")
        except Exception as error:
            await ctx.send("Unable to reload specified extension")
            self.logger.exception(error)

    @commands.command()
    async def load(self, ctx, cog):
        c = "cogs." + cog
        try:
            await self.bot.load_extension(c)
            await ctx.send(f"Successfully loaded `{cog}`")
        except Exception as error:
            await ctx.send("Unable to load extension.")
            self.logger.exception(error)

    @commands.command()
    async def unload(self, ctx, cog):
        if cog == "owner":
            await ctx.send("Unable to unload owner cog.")
            return
        c = "cogs." + cog
        try:
            await self.bot.unload_extension(c)
            await ctx.send(f"Successfully unloaded `{cog}`")
        except Exception as error:
            await ctx.send("Unable to unload extension.")
            self.logger.exception(error)


async def setup(bot):
    await bot.add_cog(Owner(bot))
