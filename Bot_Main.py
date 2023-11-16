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


async def load():
    for cog in list_cogs:
        await bot.load_extension(cog)
        print(f'Loaded {cog} cog.')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='with the API'))
    print(f'We have logged in as {bot.user}.')


@bot.command()
async def change(ctx):
    await bot.change_presence(activity=discord.Game(name='I have now changed my status!'))
    await ctx.send("I'm now playing with the API!")


# class MyHelp(commands.HelpCommand):
#
#     async def send_bot_help(self, mapping):
#         """
#         This is triggered when !help is invoked.
#
#         This example demonstrates how to list the commands that the member invoking the help command can run.
#         """
#         filtered = await self.filter_commands(self.context.bot.commands, sort=True)  # returns a list of command objects
#         names = [command.name for command in filtered]  # iterating through the commands objects getting names
#         available_commands = "\n".join(names)  # joining the list of names by a new line
#         embed = discord.Embed(description=available_commands)
#         await self.context.send(embed=embed)
#
#     async def send_command_help(self, command):
#         """This is triggered when !help <command> is invoked."""
#         await self.context.send(command.help)
#
#     async def send_group_help(self, group):
#         """This is triggered when !help <group> is invoked."""
#         await self.context.send("This is the help page for a group command")
#
#     async def send_cog_help(self, cog):
#         """This is triggered when !help <cog> is invoked."""
#         commands_cog = cog.get_commands()
#         embed = discord.Embed(title=cog.qualified_name)
#         await self.context.send("This is the help page for a cog")
#
#     async def send_error_message(self, error):
#         """If there is an error, send an embed containing the error."""
#         channel = self.get_destination()  # this defaults to the command context channel
#         await channel.send(error)
#
#
# bot.help_command = MyHelp()


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
