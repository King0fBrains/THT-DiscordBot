import discord
from discord.ext import commands

class AutoPublish(commands.Cog, description="Automatically publishes messages in the specified channels"):
    def __init__(self, bot):
        self.bot = bot
        try:
            open('configs/autopublish.txt', 'r').close()
        except FileNotFoundError:
            open('configs/autopublish.txt', 'w').close()
        with open('configs/autopublish.txt', 'r') as f:
            self.channels = [int(line) for line in f]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in self.channels:
            await message.publish()

    @commands.command(name='autopublish', aliases=['ap'], brief='This command allows for automatic publishing.',
                      help='This command allows for automatic publishing. It has one argument: channel.')
    @commands.has_permissions(manage_channels=True)
    async def autopublish(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        if channel.id in self.channels:
            await ctx.send('This channel is already being auto-published.')
            return
        self.channels.append(channel.id)
        with open('configs/autopublish.txt', 'a') as f:
            f.write(f'{channel.id}\n')
        await ctx.send(f'Now auto-publishing in {channel.mention}.')

async def setup(bot):
    await bot.add_cog(AutoPublish(bot))
