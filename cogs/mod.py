import discord
from discord.ext import commands
from datetime import datetime
from mysql.connector import connect, Error


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
    async def purge(self, ctx, amount: int, channel: discord.TextChannel = None, member: discord.Member = None):
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
    async def role(self, ctx, member: discord.Member=None, role: discord.Role=None):
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
    async def warn(self, ctx, member: discord.Member, *, message=None):
        if message is None:
            message = 'No reason provided.'
        insert_warning_query = "INSERT INTO warnings (id, warning) VALUES (%s, %s)"
        warnings = [(member.id, message)]
        embed_dm = discord.Embed(title=f'You have been warned.', description=f'Reason: {message}', colour=discord.Colour.dark_red())
        await member.send(embed=embed_dm)
        embed = discord.Embed(title=f'Warned {member}', description=f'Reason: {message}', colour=discord.Colour.dark_red())
        time = datetime.now().strftime("%d/%m/%Y")
        embed.set_footer(text=f'Warned by {ctx.author} at {time}')
        await ctx.send(embed=embed)
        channel = self.bot.get_channel(1074723158889873418)
        await channel.send(embed=embed)

        with open("configs/mysql.txt", "r") as f:
            configs = f.read().splitlines()
        try:
            with connect(
                    host="localhost",
                    user=configs[0],
                    password=configs[1],
                    database="warnings",
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(insert_warning_query, warnings)
                    connection.commit()
        except Error as e:
            print(e)
            await ctx.send('Error with the database.')

    @commands.command(name='warnings', brief='This command lists all of the warnings for a member.', help='This command lists all of the warnings for a member. It has one argument: member.')
    @commands.has_permissions(ban_members=True)
    async def warnings(self, ctx, member: discord.Member):
        ID = member.id
        select_warnings_query = (f"SELECT * FROM warnings WHERE id = {ID};")
        with open("configs/mysql.txt", "r") as f:
            configs = f.read().splitlines()
        try:
            with connect(
                    host="localhost",
                    user=configs[0],
                    password=configs[1],
                    database="warnings",
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(select_warnings_query)
                    embed = discord.Embed(title=f'Warnings for {member}', colour=discord.Colour.dark_red())
                    for warning in cursor:
                        embed.add_field(name=f'Warning {warning[0]}', value=f'{warning[2]}', inline=False)
                    await ctx.send(embed=embed)
        except Error as e:
            print(e)
            await ctx.send('Error with the database.')


async def setup(bot):
    await bot.add_cog(Mod(bot))
