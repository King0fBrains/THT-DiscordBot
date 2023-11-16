from discord.ext import commands
import pyautogui


class Click(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    Possible_Keys = ['a', 'b', 'up', 'down', 'left', 'right', 'start', 'select', 'l', 'r']
    for item in Possible_Keys:
        item.strip("'")


    @commands.Cog.listener()
    async def on_ready(self):
        print('Game is ready.')

    @commands.command(name='click', help="This command clicks the requested button.")
    async def click(self, ctx, arg):
        if arg in self.Possible_Keys:
            pyautogui.press(arg, interval=0.5)
            await ctx.send(f'Pressed the requested button: {arg}')
        else:
            await ctx.send(f"Invalid input. Please use one of the following: {'%s' % ', '.join(map(str, self.Possible_Keys))}.")


async def setup(bot):
    await bot.add_cog(Click(bot))
