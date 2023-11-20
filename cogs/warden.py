import discord
from discord.ext import commands
from pregex.core.quantifiers import Optional
from pregex.core.groups import Capture
from pregex.core.pre import Pregex
import re


class Warden(commands.Cog, description="A home for all of our warden rules."):
    def __init__(self, bot):
        self.bot = bot
        self.bot.channels = [906739960084856832, 808182861571686430, 1029842105423626250]
        self.regex_trade = re.compile('(?i)[\\.]trade')
        self.regex_t = re.compile('(?i)[\\.]t')
        self.regex_prefix = re.compile('(?i)([?,!@#$%^&*+-]t)')

    @commands.Cog.listener()
    async def on_message(self, message):
        roles = [role.id for role in message.author.roles]
        if message.channel.id != 1029842105423626250:
            return
        if message.author.bot:
            return
        if (bool(self.regex_trade.match(message.content)) or bool(self.regex_t.match(message.content))) & message.channel.id != 808182861571686430:
            embed = discord.Embed(title="Anti-Trade",
                                  description=f"User - {message.author.name} used a trade command outside of the trade channels",
                                  color=discord.Color.red())
            embed.add_field(name="Message", value=message.content, inline=False)
            await message.channel.send(embed=embed, content=f"{message.author.mention}")
            return
        if 878727109143580683 in roles or 993305944412921967 in roles or 810013892670521364 in roles:
            return
        if bool(self.regex_prefix.match(message.content)):
            embed = discord.Embed(title="Anti-Trade",
                                  description=f"User - {message.author.name} used the wrong trade command outside of the trade channels",
                                  color=discord.Color.red())
            embed.add_field(name="Message", value=message.content, inline=False)
            await message.channel.send(embed=embed, content=f"{message.author.mention}")

async def setup(bot):
    await bot.add_cog(Warden(bot))
