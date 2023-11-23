import discord
from discord.ext import commands
import logging
from datetime import datetime
from database import select_warning, insert_warning, clear_warn, insert_ban, insert_kick, select_modlog, open_config


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invite = 'https://discord.gg/V9yYzugtmr'
        self.log = logging.getLogger('discord')
        self.modlog_channel = int(open_config()['bot']['modlog'])
        self.modlog = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.modlog = self.bot.get_channel(self.modlog_channel)

    @commands.command(name="kick", brief="This command kicks a member.",
                      help="This command kicks a member. It has two arguments: member and reason.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member or int, *, message=None):
        if isinstance(member, int):
            member = self.bot.fetch_user(member)
        if message is None:
            message = 'No reason provided.'
        embed_dm = discord.Embed(title=f'You have been kicked. Please rejoin at {self.invite}',
                                 description=f'Reason: {message}', colour=discord.Colour.dark_red())
        await member.send(embed=embed_dm)
        await member.kick()
        if not insert_kick(member.id, message, ctx.author.name):
            await ctx.send('Error with the database.')
            return
        case = select_modlog(member.id)[-1][0]

        embed = discord.Embed(title=f'Case #{case} Kicked {member}', description=f'Reason: {message}',
                              colour=discord.Colour.dark_red())
        time = datetime.now().strftime("%d/%m/%Y")
        embed.set_footer(text=f'Kicked by {ctx.author} at {time}')
        await ctx.send(embed=embed)
        await self.modlog.send(embed=embed)

    @commands.command(name="ban", brief="This command bans a member.",
                      help="This command bans a member. It has two arguments: member and reason.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member or int, *, message=None):
        if isinstance(member, int):
            member = self.bot.fetch_user(member)
        if message is None:
            message = 'No reason provided.'
        embed_dm = discord.Embed(title=f'You have been banned.', description=f'Reason: {message}',
                                 colour=discord.Colour.dark_red())
        ban = insert_ban(member.id, message, ctx.author.name)
        case = select_modlog(member.id)[-1][0]
        if not ban:
            await ctx.send('Error with the database.')
            return
        await member.send(embed=embed_dm)
        await member.ban()
        embed = discord.Embed(title=f'Case #{case} Banned {member}', description=f'Reason: {message}',
                              colour=discord.Colour.dark_red())
        time = datetime.now().strftime("%d/%m/%Y")
        embed.set_footer(text=f'Banned by {ctx.author} at {time}')
        await ctx.send(embed=embed)
        await self.modlog.send(embed=embed)

    # @commands.command(name="unban", brief="This command unbans a member.",
    #                   help="This command unbans a member. It has two arguments: member and reason.")
    # @commands.has_permissions(ban_members=True)
    # async def unban(self, ctx, user:discord.User.id, *, message=None):
    #     ban_entry = await ctx.guild.fetch_ban(discord.Object(user))
    #     await ctx.guild.unban(ban_entry.user)
    #     embed = discord.Embed(title=f'Unbanned {user}', description=f'Reason: {message}',
    #                           colour=discord.Colour.dark_red())
    #     time = datetime.now().strftime("%d/%m/%Y")
    #     embed.set_footer(text=f'Unbanned by {ctx.author} at {time}')
    #     await ctx.send(embed=embed)
    #     channel = self.bot.get_channel(1074723158889873418)
    #     await channel.send(embed=embed)

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
    async def purge(self, ctx, amount: int, channel: discord.TextChannel = None, member: discord.Member or int = None):
        if isinstance(member, int):
            member = self.bot.fetch_user(member)
        if channel is None:
            channel = ctx.channel
        if member is None:
            await ctx.message.add_reaction('✅')
            await channel.purge(limit=amount+1)
        else:
            def check(message):
                return message.author == member

            await channel.purge(limit=amount+1, check=check)
        await ctx.send(f'Deleted {amount} messages.')

    @commands.command(name='role', brief='This command allows for addition/removal of roles.', help='This command allows for addition/removal of roles. It has two arguments: member and role. An example is shown below:\n\n `[p]role @member role`')
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member or int=None, role: discord.Role=None):
        if isinstance(member, int):
            member = self.bot.fetch_user(member)
        if member == ctx.author:
            await ctx.send('You cannot add/remove roles from yourself.')
            return
        if member == self.bot.user:
            await ctx.send('You cannot add/remove roles from me.')
            return
        if role is None:
            await ctx.send('Please add a role.')
            return
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f'Removed {role} from {member}.')
        else:
            try:
                await member.add_roles(role)
                await ctx.send(f'Added {role} to {member}.')
            except commands.errors.RoleNotFound:
                await ctx.send('Invalid role.')
            except commands.errors.MemberNotFound:
                await ctx.send('Invalid member')

    @commands.command(name='warn', brief='This command warns a member.', help='This command warns a member. It has two arguments: member and reason.')
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member or int, *, message=None):
        if isinstance(member, int):
            member = self.bot.fetch_user(member)
        if message is None:
            message = 'No reason provided.'
        insert_warning(member.id, message, ctx.author.name)
        case = select_warning(member.id)[-1][0]
        embed_dm = discord.Embed(title=f'You have been warned.', description=f'Reason: {message}', colour=discord.Colour.dark_red())
        await member.send(embed=embed_dm)
        embed = discord.Embed(title=f'Case #{case} Warned {member}', description=f'Reason: {message}', colour=discord.Colour.dark_red())
        time = datetime.now().strftime("%d/%m/%Y")
        embed.set_footer(text=f'Warned by {ctx.author} at {time}')
        await ctx.send(embed=embed)
        await self.modlog.send(embed=embed)
        if len (select_warning(member.id)) == 5:
            await ctx.invoke(self.bot.get_command('ban'), member=member, message='You have reached 5 warnings') #44



    @commands.command(name='warnings', brief='This command lists all of the warnings for a member.', help='This command lists all of the warnings for a member. It has one argument: member.')
    @commands.has_permissions(ban_members=True)
    async def warnings(self, ctx, member: discord.Member or int):
        if isinstance(member, int):
            member = self.bot.fetch_user(member)
        warnings = select_warning(member.id)
        if len(warnings) == 0:
            await ctx.send('No warnings found.')
            return
        embed = discord.Embed(title=f'Warnings for {member}', colour=discord.Colour.dark_red())
        for warning in warnings:
            embed.add_field(name=f'Case #{warning[0]}', value=f'{warning[2]} - By {warning[3]}', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='clearwarn', brief='This command clears a warnings for a member.', help='This command clears a warnings from a member. It has two arguments: member and case #.')
    @commands.has_permissions(ban_members=True)
    async def clearwarn(self, ctx, member: discord.Member or int, case: int):
        if isinstance(member, int):
            member = self.bot.fetch_user(member)
        warnings = select_warning(member.id)
        for warn in warnings:
            if warn[0] == case:
                clear_warn(case)
                break
        embed = discord.Embed(title=f'Cleared warning with Case # {case} for {member}', colour=discord.Colour.dark_red())
        embed.set_footer(text=f'Cleared by {ctx.author}')
        await ctx.send(embed=embed)
        await self.modlog.send(embed=embed)

    @commands.command(name='cases', brief='This command lists all of the cases for a member.', help='This command lists all of the cases for a member. It has one argument: member.')
    @commands.has_permissions(ban_members=True)
    async def cases(self, ctx, member: discord.Member or int):
        if isinstance(member, int):
            member = self.bot.fetch_user(member)
        cases = select_modlog(member.id)
        if len(cases) == 0:
            await ctx.send('No cases found.')
            return
        embed = discord.Embed(title=f'Cases for {member}', colour=discord.Colour.dark_red())
        for case in cases:
            embed.add_field(name=f'Case #{case[0]} - {case[4]}', value=f'{case[2]} - By {case[3]}', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='kickwarn', brief='This command kicks a member.', help='This command kicks a member. It has two arguments: member and reason.')
    @commands.has_permissions(ban_members=True)
    async def kickwarn(self, ctx, member: discord.Member or int, *, message=None):
        if isinstance(member, int):
            member = self.bot.fetch_user(member)
        if message is None:
            message = 'No reason provided.'
        embed_dm = discord.Embed(title=f'You have been kicked. Please rejoin at {self.invite}', description=f'Reason: {message}', colour=discord.Colour.dark_red())
        await member.send(embed=embed_dm)
        await member.kick()
        if not insert_kick(member.id, message, ctx.author.name):
            await ctx.send('Error with the database.')
            return
        if not insert_warning(member.id, message, ctx.author.name):
            await ctx.send('Error with the database.')
            return
        case = select_modlog(member.id)[-1][0]
        embed = discord.Embed(title=f'Cases #{case} & #{case-1} Kicked and Warned {member}', description=f'Reason: {message}', colour=discord.Colour.dark_red())
        time = datetime.now().strftime("%d/%m/%Y")
        embed.set_footer(text=f'Kicked and Warned by {ctx.author} at {time}')
        await ctx.send(embed=embed)
        await self.modlog.send(embed=embed)
        if len (select_warning(member.id)) == 5:
            await ctx.invoke(self.bot.get_command('ban'), member=member, message='You have reached 5 warnings')

async def setup(bot):
    await bot.add_cog(Mod(bot))

