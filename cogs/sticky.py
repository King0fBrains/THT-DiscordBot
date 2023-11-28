import discord
from discord.ext import commands
from database import read_sticky, insert_sticky, delete_sticky


class Sticky(commands.Cog, description='Keeps Messages at the bottom of the channel.'):
    def __init__(self, bot):
        self.bot = bot
        self.channels = []
        self.channels_ids = []
        self.channel_info = []
        self.load_channels = 0

        raw_list = read_sticky()
        for i in range(len(raw_list)):
            self.channels.append([raw_list[i][0], raw_list[i][1]])
            self.channels_ids.append(raw_list[i][0])

    def refresh_channels(self):
        self.channels = []
        raw_list = read_sticky()
        for i in range(len(raw_list)):
            self.channels.append([raw_list[i][0], raw_list[i][1]])

    @commands.Cog.listener()
    async def on_ready(self):
        for i in range(len(self.channels)):
            self.channel_info.append(self.bot.get_channel(self.channels[i][0]))

    @commands.Cog.listener()
    async def on_message(self, message):

        def is_me(m):
            return m.author == self.bot.user

        if message.author == self.bot.user:
            return
        if message.channel.id not in self.channels_ids:
            return
        if any(x in message.author.roles for x in
               [878727109143580683, 810013892670521364, 993305944412921967]):  # , 1003816787181314109]):
            return

        index = self.channels_ids.index(message.channel.id)
        message_content = self.channels[index][1]

        await message.channel.purge(limit=2, check=is_me)
        await message.channel.send(message_content)

    @commands.group()
    @commands.has_permissions(manage_messages=True)
    async def sticky(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid subcommand passed...')

    @sticky.command(name='add', brief="Adds a channel to the sticky channels",
                    help="Adds a channel to the sticky channels. It has two arguments: channel and message."
                         " \nAn example is shown below:"
                         "\n\n `[p]sticky add #bot ben is a nerd`")
    async def add(self, ctx, channel: discord.TextChannel, *, message: str):
        try:
            delete_sticky(channel.id)
        except Exception:
            pass
        insert_sticky(channel.id, message)
        self.refresh_channels()
        await ctx.send(f'Added {channel.name} to the sticky channels.')

    @sticky.command(name='remove', brief="Removes a channel from the sticky channels",
                    help="Removes a channel from the sticky channels. It has one argument: channel."
                         " \nAn example is shown below:"
                         "\n\n `[p]sticky remove #bot`")
    async def remove(self, ctx, channel: discord.TextChannel):
        delete_sticky(channel.id)
        self.refresh_channels()
        await ctx.send(f'Removed {channel.name} from the sticky channels.')

    @sticky.command(name='channels', brief="Displays channels that have a sticky message",
                    help="Displays channels that have a sticky message")
    async def channels(self, ctx):
        embed = discord.Embed(title='Sticky Channels', description='These are the sticky channels.',
                              colour=discord.Colour.dark_red())
        for i in range(len(self.channels)):
            embed.add_field(name=self.channel_info[i].name, value=f"Message - {self.channels[i][1]}", inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Sticky(bot))
