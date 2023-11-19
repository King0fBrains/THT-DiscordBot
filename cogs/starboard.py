import discord
from discord.ext import commands


class Starboard(commands.Cog, description='Allows for management of the starboard.'):
    def __init__(self, bot):
        self.bot = bot
        self.starboard = 1175910286646059159
        self.threshold = 5
        try:
            open('configs/starboard.txt', 'r').close()
        except FileNotFoundError:
            open('configs/starboard.txt', 'w').close()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        embed = discord.Embed(title=f"{message.author.name}", description=f"{message.content}\n\n {message.jump_url}",
                              color=discord.Color.gold())
        embed.set_footer(text=f"#{message.channel.name}, at {message.created_at.strftime('%d/%m/%Y')}")
        embed.set_thumbnail(url=message.author.display_avatar.url)
        if payload.channel_id == 1175910286646059159:
            return
        if payload.emoji.name != '⭐':
            return
        channel = self.bot.get_channel(self.starboard)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        if reaction.count < self.threshold:
            await self.bot.get_channel(payload.channel_id).send(f'⭐{reaction.count}')
            return
        elif reaction.count == self.threshold:
            print('test')
            await channel.send(embed=embed, content=f'⭐{reaction.count}')
            with open('configs/starboard.txt', 'a') as f:
                f.write(f'{message.id} {channel.last_message_id}\n')
        elif reaction.count > self.threshold:
            with open('configs/starboard.txt', 'r') as f:
                for line in f:
                    split = line.split()
                    if split[0] == str(message.id):
                        old_message = await channel.fetch_message(split[1])
                        await old_message.edit(content=f'⭐{reaction.count}', embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        embed = discord.Embed(title=f"{message.author.name}", description=f"{message.content}\n\n {message.jump_url}",
                              color=discord.Color.gold())
        embed.set_footer(text=f"#{message.channel.name}, at {message.created_at.strftime('%d/%m/%Y')}")
        embed.set_thumbnail(url=message.author.display_avatar.url)
        if reaction.count < self.threshold:
            return
        elif reaction.count >= self.threshold:
            with open('configs/starboard.txt', 'r') as f:
                for line in f:
                    split = line.split()
                    if split[0] == str(message.id):
                        channel = self.bot.get_channel(self.starboard)
                        old_message = await channel.fetch_message(split[1])
                        await old_message.edit(content=f'⭐{reaction.count}', embed=embed)


async def setup(bot):
    await bot.add_cog(Starboard(bot))
