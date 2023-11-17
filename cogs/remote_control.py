from discord.ext import commands
import pyautogui


class RemoteControl(commands.Cog, description='This is a cog for the remote control commands.'):
    Keys = ['z', 'x', 'up', 'down', 'left', 'right', 'enter', 'backspace', 'a', 's']
    Roles = (878727109143580683, 810013892670521364, 993305944412921967, 1003816787181314109)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Remote Control is ready.')

    def __init__(self, bot):
        self.bot = bot
        self.status = 2
        self.state = False

    @commands.command(name='remote',
                      brief="This command allows for admins/moderators to manage the remote control state.",
                      help="This command allows for admins/moderators to manage the remote control state.\n "
                           "The possible arguments are *on*, *off*, *all*, *admin*, and *status*.\n "
                           "*on* and *off* enable and disable the remote control respectively.\n "
                           "*all* and *admin* enable the remote control for all users and admins respectively.\n "
                           "*status* tells you whether the remote control is enabled or disabled.\n An example is shown below:\n\n `[p]remote on`")
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
            await ctx.send(f'Remote control is currently {"enabled" if self.status == 1 else "disabled"}. '
                           f'The users who have access are {"everyone" if self.status == 1 else "admins"}')
        else:
            await ctx.send('Invalid input. Please use either "on" or "off".')

    @commands.command(name='press', brief="This command clicks the requested button.",
                      help="This command clicks the requested button.\n The possible arguments are *z*, *x*, *up*, *down*, *left*, *right*, *enter*, *backspace*, *a*, and *s*.\n An example is shown below:\n\n `[p]press z`")
    async def press(self, ctx, key):
        status = self.status
        state = self.state
        keys = self.Keys

        if state is False:
            await ctx.send(f"Remote control is disabled.")
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
