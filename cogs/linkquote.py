import discord
from discord.ext import commands
from pregex.core.quantifiers import Optional
from pregex.core.groups import Capture
from pregex.core.pre import Pregex


class LinkQuote(commands.Cog, description="This cog allows for link-quoting."):
    def __init__(self, bot):
        self.bot = bot
        http_protocol = Optional('http' + Optional('s') + '://')
        domain_name = 'discord.com/channels/'

        pre: Pregex = \
            http_protocol + \
            Capture(domain_name)
        self.regex = pre

    @commands.Cog.listener()
    async def on_message(self, message):  # When a message is sent
        if message.author.bot:
            return
        if self.regex.get_matches(message.content):
            matches = message.content.split('/')
            message_linked = await message.channel.fetch_message(matches[-1])
            embed = discord.Embed(title=f"{message_linked.author.name}",
                                  description=f"{message_linked.content}\n\n {message_linked.jump_url}",
                                  color=message.author.color)
            embed.set_thumbnail(url=message_linked.author.display_avatar.url)
            await message.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(LinkQuote(bot))
