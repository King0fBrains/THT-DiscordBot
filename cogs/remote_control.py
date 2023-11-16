from discord.ext import commands
import pyautogui


class RemoteControl(commands.Cog):
    Keys = ['z', 'x', 'up', 'down', 'left', 'right', 'enter', 'backspace', 'a', 's']
    Roles = (878727109143580683, 810013892670521364, 993305944412921967, 1003816787181314109)

    def __init__(self, bot):
        self.bot = bot
        self.status = 2
        self.state = False

    @commands.command(name='remote',
                      help="This command allows for admins/moderators to manage the remote control state.",
                      brief="This command enables and disables mass remote control.")
    @commands.has_any_role(878727109143580683, 810013892670521364, 993305944412921967, 1003816787181314109)
    async def remote(self, ctx, arg):
        if arg == 'on':
            self.state = True
            await ctx.send('Remote control enabled.')
        elif arg == 'off':
            self.state = False
            await ctx.send('Remote control disabled.')
        elif arg == 'all':
            self.status = 1
            await ctx.send('Remote control enabled for all users.')
        elif arg == 'admin':
            self.status = 2
            await ctx.send('Remote control enabled for admins.')
        elif arg == 'status':
            await ctx.send(f'Remote control is currently {"enabled" if self.status == 1 else "disabled"}.')
        else:
            await ctx.send('Invalid input. Please use either "on" or "off".')

    @commands.command(name='press', brief="This command clicks the requested button.")
    async def press(self, ctx, key):
        status = self.status
        state = self.state
        keys = self.Keys
        roles = self.Roles

        if state is False:
            await ctx.send(f"Remote state is not on")
        elif status == 1:
            if key in keys:
                pyautogui.press(key, interval=0.5)
                await ctx.send(f'Pressed the requested button: {key}')
            else:
                await ctx.send(
                    f"Invalid input. Please use one of the following: {'%s' % ', '.join(map(str, keys))}.")
        else:
            if commands.has_any_role(878727109143580683, 810013892670521364, 993305944412921967,
                                     1003816787181314109) and key in keys:
                pyautogui.press(key, interval=0.5)
                await ctx.send(f'Pressed the requested button: {key}')
            elif not commands.has_any_role(878727109143580683, 810013892670521364, 993305944412921967,
                                           1003816787181314109):
                await ctx.send(f"You do not have permission to use this command.")

            else:
                await ctx.send(
                    f"Invalid input. Please use one of the following: {'%s' % ', '.join(map(str, keys))}.")


async def setup(bot):
    await bot.add_cog(RemoteControl(bot))
