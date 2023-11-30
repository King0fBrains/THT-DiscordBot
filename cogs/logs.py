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
stat        self.logging_channel = self.bot.get_channel(self.channel_id)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        emb = discord.Embed(title=f"{member.name}  has joined the guild", colour=discord.Colour.green())
        emb.timestamp = member.joined_at
        date = member.created_at.strftime("%m/%d/%Y")
        emb.set_thumbnail(url=member.display_avatar)
        emb.add_field(name="**Member**", value=member.mention, inline=True)
        emb.add_field(name="**Member ID**", value=f"`{member.id}`", inline=True)
        emb.add_field(name="**Total Users**", value=member.guild.member_count, inline=True)
        emb.add_field(name="**Account Created on:**", value=date, inline=True)
        await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        emb = discord.Embed(title=f"{member.name} has left the guild", color=discord.Colour.red())
        emb.timestamp = datetime.now()
        emb.set_thumbnail(url=member.display_avatar)
        emb.add_field(name="**Member**", value=member.mention, inline=True)
        emb.add_field(name="**Member ID**", value=f"`{member.id}`", inline=True)
        emb.add_field(name="**Total Users**", value=member.guild.member_count, inline=True)
        await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.id != self.bot.user.id:
            user = message.author
            emb = discord.Embed(colour=discord.Colour.red())
            emb.timestamp = datetime.now()

            emb.description = f"> {message.content}"
            emb.set_author(name=f"{user.name}  ({user.id}) | Deleted message", icon_url=message.author.display_avatar)
            emb.add_field(name="**Channel**", value=message.channel.mention, inline=True)
            emb.add_field(name="**Member**", value=message.author.mention, inline=True)
            emb.add_field(name="**Message ID**", value=f"`{message.id}`", inline=True)

            if len(message.attachments) != 0:
                out = " "
                for i in message.attachments:
                    out += f"`{i.filename}`\n"
                emb.add_field(name="**Attachment(s)**", value=out)

            await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_message_edit(self, origin: discord.Message, edit: discord.Message):
        if origin.author.id != self.bot.user.id:
            if not origin.author.bot:
                emb = discord.Embed(colour=discord.Colour.orange())
                emb.timestamp = datetime.now()
                emb.description = f"**Original Message**:\n> {origin.content}\n\n**Edited Message**:\n> {edit.content}"
                emb.set_author(name=f"{origin.author.name}  ({origin.author.id}) | Message edited",
                               icon_url=origin.author.display_avatar)
                emb.add_field(name="**Channel**", value=origin.jump_url, inline=True)
                emb.add_field(name="**Member**", value=origin.author.mention, inline=True)
                emb.add_field(name="**Message ID**", value=f"`{origin.id}`", inline=True)
                await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        emb = discord.Embed(colour=discord.Colour.fuchsia())
        emb.timestamp = role.created_at
        emb.description = role.name
        emb.set_author(name=f"New Role created ({role.id})")
        emb.add_field(name="**Role**", value=role.mention)
        emb.add_field(name="**Role ID**", value=role.id)
        await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        emb = discord.Embed(colour=discord.Colour.red())
        emb.timestamp = datetime.now()
        emb.description = role.name
        emb.set_author(name=f"Role Deleted ({role.id})")
        emb.add_field(name="**Role ID**", value=role.id)
        await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_role_update(self, origin: discord.Role, edit: discord.Role):
        emb = discord.Embed(colour=discord.Colour.orange())
        emb.timestamp = datetime.now()
        emb.description = f"**Original**\n> {origin.name}\n\n**Edit**\n> {edit.name}"
        emb.set_author(name=f"Role Edited ({origin.id})")
        emb.add_field(name="**Mention**", value=edit.mention)
        emb.add_field(name="**Role ID**", value=edit.id)
        await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        emb = discord.Embed(colour=discord.Colour.fuchsia())
        emb.timestamp = channel.created_at
        emb.description = f"> `{channel.category}` --> `{channel.name}`"
        emb.set_author(name=f"New Channel created ({channel.id})")
        emb.add_field(name="**Mention**", value=channel.mention)
        emb.add_field(name="**Channel ID**", value=channel.id)
        emb.add_field(name="**Jump**", value=channel.jump_url)
        await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        emb = discord.Embed(colour=discord.Colour.red())
        emb.timestamp = datetime.now()
        emb.description = channel.name
        emb.set_author(name=f"Channel Deleted")
        emb.add_field(name="**Channel ID**", value=channel.id)
        await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, origin: discord.abc.GuildChannel, edit: discord.abc.GuildChannel):
        # Needs to be more robust to catch more edits like permissions"
        emb = discord.Embed(colour=discord.Colour.orange())
        emb.timestamp = datetime.now()
        if origin.name != edit.name:
            emb.description = f"**Original**\n> {origin.name}\n\n**Edit**\n> {edit.name}"

        emb.set_author(name=f"Channel Edited ({origin.id})")
        emb.add_field(name="**Mention**", value=edit.mention)
        emb.add_field(name="**Channel ID**", value=edit.id)
        emb.add_field(name="**Jump**", value=edit.jump_url)
        await self.logging_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_member_update(self, origin: discord.Member, edit: discord.Member):
        emb = discord.Embed(colour=discord.Colour.orange())
        emb.set_author(name=f"{origin.name} updated their profile",
                       icon_url=origin.display_avatar)
        emb.set_thumbnail(url=edit.display_avatar)
        emb.add_field(name="**Mention**", value=origin.mention)
        emb.add_field(name="**User ID**", value=origin.id)
        emb.timestamp = datetime.now()
        await self.logging_channel.send(embed=emb)


async def setup(bot):
    await bot.add_cog(Logs(bot))
