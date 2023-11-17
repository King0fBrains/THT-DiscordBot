import discord
from discord.ext import commands
from datetime import datetime


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invite = 'https://discord.gg/V9yYzugtmr'

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mod is ready.')

    @commands.command(name="kick", brief="This command kicks a member.",
                      help="This command kicks a member. It has two arguments: member and reason.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, message=None):
        embed_dm = discord.Embed(title=f'You have been kicked. Please rejoin at {self.invite}',
                                 description=f'Reason: {message}', colour=discord.Colour.dark_red())
        await member.send(embed=embed_dm)
        await member.kick()
        embed = discord.Embed(title=f'Kicked {member}', description=f'Reason: {message}',
                              colour=discord.Colour.dark_red())
        time = datetime.now().strftime("%d/%m/%Y")
        embed.set_footer(text=f'Kicked by {ctx.author} at {time}')
        await ctx.send(embed=embed)
        channel = self.bot.get_channel(1074723158889873418)
        await channel.send(embed=embed)

    @commands.command(name="ban", brief="This command bans a member.",
                      help="This command bans a member. It has two arguments: member and reason.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, message=None):
        embed_dm = discord.Embed(title=f'You have been banned.', description=f'Reason: {message}',
                                 colour=discord.Colour.dark_red())
        await member.send(embed=embed_dm)
        await member.ban()
        embed = discord.Embed(title=f'Banned {member}', description=f'Reason: {message}',
                              colour=discord.Colour.dark_red())
        time = datetime.now().strftime("%d/%m/%Y")
        embed.set_footer(text=f'Banned by {ctx.author} at {time}')
        await ctx.send(embed=embed)
        channel = self.bot.get_channel(1074723158889873418)
        await channel.send(embed=embed)

    @commands.command(name="unban", brief="This command unbans a member.",
                      help="This command unbans a member. It has two arguments: member and reason.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, message=None):
        embed_dm = discord.Embed(title=f'You have been unbanned.', description=f'Reason: {message}',
                                 colour=discord.Colour.dark_red())
        await member.send(embed=embed_dm)
        await member.unban()
        embed = discord.Embed(title=f'Unbanned {member}', description=f'Reason: {message}',
                              colour=discord.Colour.dark_red())
        time = datetime.now().strftime("%d/%m/%Y")
        embed.set_footer(text=f'Unbanned by {ctx.author} at {time}')
        await ctx.send(embed=embed)
        channel = self.bot.get_channel(1074723158889873418)
        await channel.send(embed=embed)

    @commands.command(name='massban', aliases=['hackban'], brief='This command bans multiple members.',
                      help='This command bans multiple members. It only takes user ids.')
    @commands.has_permissions(ban_members=True)
    async def massban(self, ctx, *members):
        channel = self.bot.get_channel(1074723158889873418)
        time = datetime.now().strftime("%d/%m/%Y")
        for member in members:
            embed = discord.Embed(title=f'Banned {member}', description=f'Reason: massban',
                                  colour=discord.Colour.dark_red())
            embed.set_footer(text=f'Banned by {ctx.author} at {time}')
            await channel.send(embed=embed)
            await ctx.guild.ban(discord.Object(id=int(member)))
        await ctx.send('Banned all the members.')

    @commands.command(name='purge', aliases=['cleanup'], brief='This command deletes messages.',
                      help='This command deletes messages.')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, channel: discord.TextChannel = None, member: discord.Member = None, amount: int = 5):
        if channel is None:
            channel = ctx.channel
        if member is None:
            await channel.purge(limit=amount)
        else:
            def check(message):
                return message.author == member

            await channel.purge(limit=amount, check=check)
        await ctx.send(f'Deleted {amount} messages.')


async def setup(bot):
    await bot.add_cog(Mod(bot))
