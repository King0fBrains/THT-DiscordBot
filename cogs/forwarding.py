import discord
import json

from datetime import datetime
from discord.ext import commands


class Forwarding(commands.Cog, description='Allows for forwarding messages from dms to a channel.'):
    def __init__(self, bot):
        self.bot = bot
        with open("config.json") as c:
            config = json.load(c)
            self.channel_id = int(config['bot']['forwarding'])
            self.forward_channel = self.bot.get_channel(self.channel_id)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        if message.guild is None:
            emb = discord.Embed(color=discord.Color.gold())
            emb.timestamp = datetime.now()
            emb.set_author(name=f"{message.author.name} ({message.author.id})",
                           icon_url=message.author.display_avatar)
            emb.description = message.content

            if len(message.attachments) != 0:
                for i in message.attachments:
                    emb.description += f"\n> {i.proxy_url}\n"

            await self.forward_channel.send(embed=emb)
            await message.add_reaction('✅')

    @commands.command(name='dm', aliases=['pm'], brief='This command sends a dm to a user.',
                      help='This command sends a dm to a user. It has 2 arguments. The User and the Message.')
    @commands.has_any_role(878727109143580683, 810013892670521364, 993305944412921967, 1003816787181314109)
    async def dm(self, ctx, user: discord.User, *, message):
        if ctx.author.id == self.bot.user.id:
            return
        emb = discord.Embed(title='DM', description=message, color=discord.Color.gold())
        emb.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.display_avatar)
        await user.send(embed=emb, files=[await attachment.to_file() for attachment in ctx.message.attachments])
        await ctx.message.add_reaction('✅')


async def setup(bot):
    await bot.add_cog(Forwarding(bot))
