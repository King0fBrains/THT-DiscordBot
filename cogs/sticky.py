import discord
from discord.ext import commands


class Sticky(commands.Cog, description='Keeps Messages at the bottom of the channel.'):
    def __init__(self, bot):
        self.bot = bot
        self.channels = []
        self.channel_info = []
        self.channel_type = []

        try:
            open('configs/sticky.txt', 'r').close()
        except FileNotFoundError:
            open('configs/sticky.txt', 'w').close()

        with open('configs/sticky.txt', 'r') as f:
            for line in f:
                split = line.split()
                self.channels.append([int(split[0]), split[1]])

    @commands.Cog.listener()
    async def on_ready(self):
        for i in range(len(self.channels)):
            self.channel_info.append(self.bot.get_channel(self.channels[i][0]))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.channel not in self.channel_info:
            return
        if any(x in message.author.roles for x in
               [878727109143580683, 810013892670521364, 993305944412921967]):  # , 1003816787181314109]):
            await message.channel.send('2')
            return

        def is_me(m):
            return m.author == self.bot.user

        pokemon = '**Make sure you have read <#1089543609046536192> and <#1089543423989645402> before requesting any Pokémon. BOT CAN NOT CURRENTLY MAKE EGGS**'
        anch_order = '**This channel is only for requesting/ordering! Do not look up items here. Make sure you have read <#1080859952769421333> and <#1080859998155968553> before requesting any items.**'
        anch_info = '**This channel is for looking up items ONLY! Make sure you have read <#1080859952769421333> and <#1080859998155968553>. Absolutely no ordering in this channel. All orders are to be done in <#1080860091277901925>.**'
        help_info = '**Be specific and detailed when asking your question. Any questions already answered in the rules, tutorials, and faqs will be ignored.**'
        vip = '**Check out <#1090249780975902751> to get access to this channel.\nMake sure you have read <#1089543609046536192> and <#1089543423989645402> before requesting any Pokémon. BOT CAN NOT CURRENTLY MAKE EGGS**'
        raid = "**Join as much as you want. Be considerate of others. Bot will rotate about 75 different mons. Ping Abel/Harambae in <#808182861571686430 if the bot breaks. Don't be a lil bitch."
        await message.channel.purge(limit=1, check=is_me)
        if self.channels[self.channel_info.index(message.channel)][1] == 'bot':
            await message.channel.send(pokemon)
        elif self.channels[self.channel_info.index(message.channel)][1] == 'order':
            await message.channel.send(anch_order)
        elif self.channels[self.channel_info.index(message.channel)][1] == 'info':
            await message.channel.send(anch_info)
        elif self.channels[self.channel_info.index(message.channel)][1] == 'help':
            await message.channel.send(help_info)
        elif self.channels[self.channel_info.index(message.channel)][1] == 'vip':
            await message.channel.send(vip)
        elif self.channels[self.channel_info.index(message.channel)][1] == 'raid':
            await message.channel.send(raid)

    @commands.command(name='channels', brief="Displays channels that have a sticky message", help="Displays channels that have a sticky message")
    @commands.has_permissions(manage_messages=True)
    async def channels(self, ctx):
        embed = discord.Embed(title='Sticky Channels', description='These are the sticky channels.',
                              colour=discord.Colour.dark_red())
        for i in range(len(self.channels)):
            embed.add_field(name=self.channel_info[i].name, value=f"Type - {self.channels[i][1]}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='add_channel', brief="Adds a channel to the sticky channels",
                      help="Adds a channel to the sticky channels. It has two arguments: channel and channel_type."
                           "\nPossible channel types are *bot*, *order*, *info*, *help*, *vip*, and *raid*. An example is shown below:"
                           "\n\n `[p]add_channel #bot bot`")
    @commands.has_permissions(manage_messages=True)
    async def add_channel(self, ctx, channel: discord.TextChannel, channel_type):
        if channel_type not in ['bot', 'order', 'info', 'help', 'vip', 'raid']:
            await ctx.send('Invalid channel type.')
            return
        self.channels.append([channel.id, channel_type])
        self.channel_info.append(channel)
        with open('configs/sticky.txt', 'a') as f:
            f.write(f'{channel.id} {channel_type}\n')
        await ctx.send(f'Added {channel.name} to the sticky channels.')

async def setup(bot):
    await bot.add_cog(Sticky(bot))
