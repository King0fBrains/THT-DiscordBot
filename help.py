import discord
from discord.ext import commands
from discord.ext.commands import Cog, Command



class MyHelp(commands.HelpCommand):  # Custom Help Command

    async def send_bot_help(self, mapping: dict[Cog, list[Command]]):
        f_mapping = {}
        for cog, cmds in mapping.items():
            if cog and (f_cmds := await self.filter_commands(cmds, sort=True)):
                f_mapping[cog] = f_cmds

        # list_cogs1 = [f'**{list_cogs1[i]}** - {list_descriptions[i]}' for i in range(len(list_cogs1))]
        # list_cogs1 = '\n'.join(list_cogs1)
        embed = discord.Embed(title='List Of Cogs', color=discord.Color.green())
        for cog in f_mapping:
            embed.add_field(name=cog.qualified_name, value='\n'.join([f'*{cmd.name}* - {cmd.brief}' for cmd in f_mapping[cog]]), inline=False)
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


