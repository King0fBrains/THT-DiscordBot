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

if not os.path.exists('configs'):  # Create the config directory if it doesn't exist
    os.mkdir('configs')


async def everyone_ping():
    await bot.wait_until_ready()
    while not bot.is_closed():
        channel = bot.get_channel(775883912760918036)
        await channel.send("@everyone\nDon't forget to join The High Table!\n"
                           "We have free genning bots that run 24/7 for Scarlet/Violet, SWSH, BDSP, and PLA we also have an Animal Crossing New Horizons Bot!!!\n"
                           "Join now and complete your shiny dex!!!\n"
                           "Vergesst nicht dem High Table beizutreten!\n"
                           "Wir haben kostenlose genning bots die 24/7 für Karmesin/Purpur, SWSH, BDSP, Animal Crossing New Horizon bot.\n"
                           "Tritt jetzt bei um dir deinen Shiny dex zu komplettieren.\n"
                           "Dies ist ein Englisch sprechender Server, trotzdem funktionieren die bots gleich.\n"
                           "discord.gg/tht")
        await asyncio.sleep(3600)


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
    bot.loop.create_task(everyone_ping())


try:  # Create the logs directory if it doesn't exist
    open('logs/discord.log', 'r').close()
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
