import discord
import asyncio
import logging
import logging.handlers
import json
import sys
import os

from discord.ext import commands
from os.path import isfile, join
from datetime import datetime
from help import MyHelp
from database import create_modlog, create_db

def get_logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    log_dir = os.path.join(os.getcwd() + os.sep + '/logs')

    handler = logging.handlers.RotatingFileHandler(
        filename=log_dir + '/discord.log',
        encoding='utf-8',
        backupCount=5,  # Rotate through 5 files
    )
    
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def make_logs():
    try:  # Create the logs directory if it doesn't exist
        open('logs/discord.log', 'r').close()
    except FileNotFoundError:
        print("Creating log directory.")
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
    
if __name__ == "__main__":
    make_logs()
    log = get_logger()
    log.info("Starting main bot loop")
    
    try:
        with open("config.json") as c:
            config = json.load(c)
            intents = discord.Intents.all()
            intents.members = True
            bot = commands.Bot(command_prefix=config['bot']['prefix'], intents=intents)
            bot.help_command = MyHelp()
    except FileNotFoundError:
        log.critical("No config file found. Please makes sure 'config.json' is in your active directory")
        sys.exit(0)

    if not os.path.exists('configs'):  # Create the config directory if it doesn't exist
        try:
            os.mkdir('configs')
        except PermissionError:
            log.error(PermissionError)
            
    try:
        create_db()
        create_modlog()
    except Exception as e:
        log.error(e)
        sys.exit(0)

async def everyone_ping():
    await bot.wait_until_ready()
    while not bot.is_closed():
        servers = [guild.id for guild in bot.guilds]
        if 720439033355829268 in servers:
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
        else:
            log.error("Unable to constantly ping Germans!")
            return

async def load():  # Load all the cogs
    for cog in ["cogs." + f.replace('.py', '') for f in os.listdir('cogs') if isfile(join('cogs', f))]:
        try:
           await bot.load_extension(cog)
           log.info(f"Cog {cog[5:]} was successfully loaded!")
        except Exception as e :
            log.exception(f'Unable to load {cog}\n{e}')

@bot.event
async def on_ready():  # When the bot come online
    log.info(f"Successfully logged in as {bot.user}")
    bot.loop.create_task(everyone_ping())
    await bot.change_presence(activity=discord.Game(name=config['bot']['status']))

async def main():
    async with bot:
        await load()
        await bot.start(config['bot']['token'])
        
asyncio.run(main())
