from discord.ext import commands
import discord


class Forwarding(commands.Cog, description='Allows for forwarding messages from dms to a channel.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Forwarding is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        if message.guild is None:
            channel = self.bot.get_channel(1029842105423626250)
            embed = discord.Embed(title='DM', description=message.content, color=discord.Color.gold())
            embed.set_footer(text=f'{message.author.name}#{message.author.discriminator}', icon_url=message.author.display_avatar)
            await channel.send(embed=embed, files=[await attachment.to_file() for attachment in message.attachments], content=f'**Id** = {message.author.id}')
            await message.add_reaction('✅')

    @commands.command(name='dm', aliases=['pm'],brief='This command sends a dm to a user.', help='This command sends a dm to a user. It has 2 arguments. The User and the Message.')
    @commands.has_any_role(878727109143580683, 810013892670521364, 993305944412921967, 1003816787181314109)
    async def dm(self, ctx, user: discord.User, *, message):
        if ctx.author.id == self.bot.user.id:
            return
        embed = discord.Embed(title='DM', description=message, color=discord.Color.gold())
        embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.display_avatar)
        await user.send(embed=embed, files=[await attachment.to_file() for attachment in ctx.message.attachments])
        await ctx.message.add_reaction('✅')

async def setup(bot):
    await bot.add_cog(Forwarding(bot))
