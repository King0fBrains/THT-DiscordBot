import discord
from discord.ext import commands
from pregex.core.quantifiers import Optional
from pregex.core.groups import Capture
from pregex.core.pre import Pregex
from pregex.core.operators import Either
import re


class Warden(commands.Cog, description="A home for all of our warden rules."):
    def __init__(self, bot):
        self.bot = bot
        self.bot.channels = [906739960084856832, 808182861571686430, 1029842105423626250]
        self.staff_channel_id = 900502871156613190
        wrong_channel = Capture('.') + (Either('t', 'T') + Optional('rade'))
        pre: Pregex = \
            wrong_channel
        self.regex_wrong_channel = pre
        self.wrong_prefix = Either('?', '!', '@', '#', '$', '%', '^', '&', '*', '+', '-') + Either('t', 'T') + Optional('rade')
        self.invite_link = re.compile(r"(discord\.(?:gg|io|me|li)|discord(?:app)?\.com\/invite)\/(\S+)", re.I)

    @commands.Cog.listener()
    async def on_ready(self):
        self.staff_channel = self.bot.get_channel(self.staff_channel_id)

    @commands.Cog.listener()
    async def on_message(self, message):
        roles = [role.id for role in message.author.roles]
        staff_channel = self.bot.get_channel(900502871156613190)
        if message.channel.id not in self.bot.channels:
            return
        if message.author.bot:
            return
        if message.channel.id == 808182861571686430:
            pass
        elif bool(self.regex_wrong_channel.get_matches(message.content)):
            embed = discord.Embed(title="Anti-Trade",
                                  description=f"User - {message.author.name} used a trade command outside of the trade channels",
                                  color=discord.Color.red())
            embed.add_field(name="Message", value=message.content, inline=False)
            embed.set_footer(text=f"{message.author.mention} in {message.jump_url}")
            await self.staff_channel.send(embed=embed)
            return
        if 878727109143580683 in roles or 993305944412921967 in roles or 810013892670521364 in roles:
            return
        pre: Pregex = \
            self.wrong_prefix
        self.regex_wrong_channel = pre
        if bool(self.regex_wrong_channel.get_matches(message.content)):
            embed = discord.Embed(title="Anti-Trade",
                                  description=f"User - {message.author.name} used the wrong trade command outside of the trade channels",
                                  color=discord.Color.red())
            embed.add_field(name="Message", value=message.content, inline=False)
            embed.set_footer(text=f"{message.author.mention} in {message.jump_url}")
            await self.staff_channel.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id != 720439033355829268:
            return
        if message.author.bot:
            return
        result = bool(self.invite_link.findall(message.content))
        if result is True:
            embed = discord.Embed(title="Anti-Invite", description=f"User {message.author.name}- {message.content} sent an invite link",
                                  color=discord.Color.red())
            embed.set_footer(text=f"{message.author.mention}")
            await self.staff_channel.send(embed=embed)
            await message.delete()

def setup(bot):
     bot.add_cog(Warden(bot))
