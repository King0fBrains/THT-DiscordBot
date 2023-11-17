import discord
import asyncio
import logging
import logging.handlers
from discord.ext import commands
import os
from os.path import isfile, join
from datetime import datetime
from help import MyHelp

with open('token.txt') as f:  # Get the token
    token = f.readline()
intents = discord.Intents.all()  # Set all the intents

bot = commands.Bot(command_prefix='.', description='we shall see where this appears', intents=intents)
bot.help_command = MyHelp()
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


@bot.event
async def on_command_error(ctx, error):  # If there is an error, send an embed containing the error.
    if isinstance(error, commands.CommandNotFound):
        return
    else:
        embed = discord.Embed(title=f'Error in command **{ctx.command}**.', description=error,
                              color=discord.Color.red())
        channel = bot.get_channel(1029842105423626250)
        await channel.send(embed=embed)
        await ctx.send(embed=embed)


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
