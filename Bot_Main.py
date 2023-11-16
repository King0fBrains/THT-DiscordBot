import discord
import asyncio
import logging
import logging.handlers
from discord.ext import commands

with open('token.txt') as f:
    token = f.readline()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='.', description='we shall see where this appears', intents=intents)

list_cogs = ['cogs.ping', 'cogs.embed_test', 'cogs.owner', 'cogs.remote_control']


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}.')


async def load():
    for cog in list_cogs:
        await bot.load_extension(cog)
        print(f'Loaded {cog} cog.')


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='with the API'))


@bot.command()
async def change(ctx):
    await bot.change_presence(activity=discord.Game(name='I have now changed my status!'))
    await ctx.send("I'm now playing with the API!")


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
