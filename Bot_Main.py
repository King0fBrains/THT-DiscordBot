import discord
import asyncio
import logging
import logging.handlers
from discord.ext import commands
import os
from os.path import isfile, join
from datetime import datetime

with open('token.txt') as f:  # Get the token
    token = f.readline()
intents = discord.Intents.all()  # Set all the intents

bot = commands.Bot(command_prefix='.', description='we shall see where this appears', intents=intents)

list_cogs = ["cogs." + f.replace('.py', '') for f in os.listdir('cogs') if isfile(join('cogs', f))]  # Get all the cogs


async def load():  # Load all the cogs
    for cog in list_cogs:
        await bot.load_extension(cog)
        print(f'Loaded {cog} cog.')


@bot.event
async def on_ready():  # When the bot come online
    await bot.change_presence(activity=discord.Game(name='Ben=Nerd'))
    channel = bot.get_channel(1029842105423626250)
    await channel.send(embed=discord.Embed(title='Bot is ready.', color=discord.Color.green()))
    print(f'We have logged in as {bot.user}.')


class MyHelp(commands.HelpCommand):  # Custom Help Command

    async def send_bot_help(self, mapping):
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
        if not command.aliases == []:
            embed.add_field(name='Aliases', value=', '.join(command.aliases), inline=False)
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

try:  # Create the logs directory if it doesn't exist
    open('logs/discord.log', 'w').close()
except FileNotFoundError:
    os.mkdir('logs')
try:  # Rename the log file if it is too large, or create the log file if it doesn't exist
    file_length = 0
    with open('logs/discord.log', 'r') as f:
        for file_length, line in enumerate(f):
            pass
    if file_length > 10000:
        os.rename('logs/discord.log', 'logs/discord-' + datetime.now().strftime('%YY-%mM-%dD-%Hh-%Mm') + '.log')
except FileNotFoundError:
    print('No log file found.')
    open('logs/discord.log', 'w').close()


async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    log_dir = os.path.join(os.getcwd() + os.sep + '/logs')

    handler = logging.handlers.RotatingFileHandler(
        filename=log_dir + '/discord.log',
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
