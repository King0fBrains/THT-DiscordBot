import json
import discord

from datetime import datetime, timedelta
from discord.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("config.json") as c:
            config = json.load(c)
            self.channel_id = int(config['bot']['serverlog'])
        self. logging_channel = self.bot.get_channel(self.channel_id)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed = discord.Embed(title=f"{member.name}  has joined the guild", colour=discord.Colour.green())
        embed.timestamp = member.joined_at
        date = member.created_at.strftime("%m/%d/%Y")

        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="**Member**", value=member.mention, inline=True)
        embed.add_field(name="**Member ID**", value=f"`{member.id}`", inline=True)
        embed.add_field(name="**Total Users**", value=member.guild.member_count, inline=True)
        embed.add_field(name="**Account Created on:**", value=date, inline=True)

        today = discord.utils.utcnow() - timedelta(days=1)
        week = discord.utils.utcnow() - timedelta(days=7)
        if member.created_at < today:
            embed.description = "> This account was created today!"
        if today < member.created_at < week:
            embed.description = "> This account was created less than one week ago!"
        await self.logging_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        embed = discord.Embed(title=f"{member.name} has left the guild", color=discord.Colour.red())
        embed.timestamp = datetime.now()
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="**Member**", value=member.mention, inline=True)
        embed.add_field(name="**Member ID**", value=f"`{member.id}`", inline=True)
        embed.add_field(name="**Total Users**", value=member.guild.member_count, inline=True)
        await self.logging_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
