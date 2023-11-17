import discord
from discord.ext import commands


class Info(commands.Cog, description='This is the home for all of the information commands.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):  # This event is called when the bot is ready
        print('Info is ready.')

    @commands.command(name='ping', brief='This command returns the latency',
                      help='This command gives the latency. It has no arguments.')
    async def ping(self, ctx):
        await ctx.send(f'**Pong!** Latency: {round(self.bot.latency * 1000)}ms')

    @commands.command(name='userinfo', brief='This command returns the user info', aliases=['ui'],
                      help='This command gives the user info. It can either be used with a mention or without any arguments.')
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title='User Info', description=f'Here is the info we retrieved about {member}',
                              color=member.color)
        embed.add_field(name='Name', value=member.name, inline=True)
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Status', value=member.status, inline=True)
        embed.add_field(name='Highest Role', value=member.top_role, inline=True)
        embed.add_field(name='Joined At', value=f'{member.joined_at.strftime("%b %d, %Y")}', inline=True)
        embed.add_field(name='Created At', value=f'{member.created_at.strftime("%b %d, %Y")}', inline=True)
        embed.set_thumbnail(url=member.display_avatar)
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo', brief='This command returns the server info',
                      help='This command gives the server info. It has no arguments.')
    async def serverinfo(self, ctx):
        embed = discord.Embed(title='Server Info', description=f'Here is the info we retrieved about {ctx.guild.name}',
                              color=discord.Color.og_blurple())
        embed.add_field(name='Name', value=ctx.guild.name, inline=True)
        embed.add_field(name='ID', value=ctx.guild.id, inline=True)
        embed.add_field(name='Owner', value=ctx.guild.owner, inline=True)
        embed.add_field(name='Created At', value=f'{ctx.guild.created_at.strftime("%b %d, %Y")}', inline=True)
        embed.add_field(name='Member Count', value=ctx.guild.member_count, inline=True)
        embed.add_field(name='Role Count', value=len(ctx.guild.roles), inline=True)
        embed.add_field(name='Emoji Count', value=len(ctx.guild.emojis), inline=True)
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)

    @commands.command(name='botinfo', brief='This command returns the bot info',
                      help='This command gives the bot info. It has no arguments.')
    async def botinfo(self, ctx):
        x = await commands.Bot.application_info(self.bot)
        embed = discord.Embed(title=f'{ctx.bot.user.name}', description=f'All about {ctx.bot.user.name}',
                              color=ctx.bot.user.color)
        embed.add_field(name='Owner', value=f'<@{x.owner.id}>', inline=True)
        embed.add_field(name='ID', value=ctx.bot.user.id, inline=True)
        embed.add_field(name='Created At', value=f'{ctx.bot.user.created_at.strftime("%b %d, %Y")}', inline=True)
        embed.add_field(name='Member Count', value=len(ctx.bot.users), inline=True)
        embed.add_field(name='Guild Count', value=len(ctx.bot.guilds), inline=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
