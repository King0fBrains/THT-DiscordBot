import discord
from discord.ext import commands
import pyautogui


class Remote_Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status = 0

    Possible_Keys = ['a', 'b', 'up', 'down', 'left', 'right', 'start', 'select', 'l', 'r']
    for item in Possible_Keys:
        item.strip("'")

    @commands.Cog.listener()
    async def on_ready(self):
        print('Game is ready.')

    @commands.command(name='remote', help="This command enables and disables mass remote control.")
    @commands.has_any_role(878727109143580683, 810013892670521364, 993305944412921967)
    async def remote(self, ctx, arg):
        if arg == 'on':
            self.status = 1
            await ctx.send('Remote control enabled.')
        elif arg == 'off':
            self.status = 0
            await ctx.send('Remote control disabled.')
        elif arg == 'admin':
            self.status = 2
            await ctx.send('Remote control enabled for admins.')
        elif arg == 'status':
            await ctx.send(f'Remote control is currently {"enabled" if self.status == 1 else "disabled"}.')
        else:
            await ctx.send('Invalid input. Please use either "on" or "off".')

    @commands.command(name='press', help="This command clicks the requested button.")
    async def press(self, ctx, arg):
        if self.status != 0:
            if self.status == 2:
                if 878727109143580683 or 810013892670521364 or 993305944412921967 in [role.id for role in ctx.author.roles]:
                    if arg in self.Possible_Keys:
                        pyautogui.press(arg, interval=0.5)
                        await ctx.send(f'Pressed the requested button: {arg}')
                    else:
                        await ctx.send(
                            f"Invalid input. Please use one of the following: {'%s' % ', '.join(map(str, self.Possible_Keys))}.")
            elif arg in self.Possible_Keys:
                pyautogui.press(arg, interval=0.5)
                await ctx.send(f'Pressed the requested button: {arg}')
            else:
                await ctx.send(f"Invalid input. Please use one of the following: {'%s' % ', '.join(map(str, self.Possible_Keys))}.")


async def setup(bot):
    await bot.add_cog(Remote_Control(bot))
