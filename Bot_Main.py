import discord
import asyncio
import logging
import logging.handlers
from discord.ext import commands
from os import listdir
from os.path import isfile, join

with open('token.txt') as f:
    token = f.readline()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='.', description='we shall see where this appears', intents=intents)

list_cogs = ["cogs." + f.replace('.py', '') for f in listdir('cogs') if isfile(join('cogs', f))]


async def load():
    for cog in list_cogs:
        await bot.load_extension(cog)
        print(f'Loaded {cog} cog.')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Ben=Nerd'))
    channel = bot.get_channel(1029842105423626250)
    await channel.send(embed=discord.Embed(title='Bot is ready.', color=discord.Color.green()))
    print(f'We have logged in as {bot.user}.')


class MyHelp(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        """
        This is triggered when !help is invoked.

        This example demonstrates how to list the commands that the member invoking the help command can run.
        """
        list_cogs1 = [bot.cogs[cog].qualified_name for cog in bot.cogs]
        list_descriptions = [bot.cogs[cog].description for cog in bot.cogs]
        list_cogs1 = [f'**{list_cogs1[i]}** - {list_descriptions[i]}' for i in range(len(list_cogs1))]
        list_cogs1 = '\n'.join(list_cogs1)
        embed = discord.Embed(title='List Of Cogs', description=list_cogs1, color=discord.Color.green())
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        """This is triggered when !help <command> is invoked."""
        command_help = command.help
        name = command.name
        embed = discord.Embed(title=name, description=command_help, color=discord.Color.red())
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        """This is triggered when !help <group> is invoked."""
        await self.context.send("This is the help page for a group command")

    async def send_cog_help(self, cog):
        """This is triggered when !help <cog> is invoked."""
        commands_cog = cog.get_commands()
        commands_cog = await self.filter_commands(commands_cog, sort=True)
        commands_combined = []
        for command in commands_cog:
            commands_combined.append(f'**{command.name}** - {command.brief}')
        commands_combined = '\n'.join(commands_combined)
        embed = discord.Embed(title=cog.qualified_name, description=commands_combined, color=discord.Color.blue())
        await self.context.send(embed=embed)

    async def send_error_message(self, error):
        """If there is an error, send an embed containing the error."""
        channel = self.get_destination()  # this defaults to the command context channel
        await channel.send(error)


bot.help_command = MyHelp()


async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    async with bot:
        await load()
        await bot.start(token)


asyncio.run(main())
