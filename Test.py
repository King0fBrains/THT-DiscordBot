import discord
import asyncio

from discord.ext import commands

token = 'OTk1MTkxNjkzNjM4OTA1OTc3.GbnSNo.Rc1pG0PSZ549tTAKCAWVzRspe6tKku9ITRxbDQ'

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='.', description='we shall see where this appears', intents=intents)

list_cogs = ['cogs.ping']


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
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())
