import discord
import ast
from discord.ext import commands
import asyncio


def insert_returns(body):
    # insert return stmt if the last expression is an expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the or-else
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return commands.is_owner()

    @commands.command(name='eval', brief='This command evaluates input.', help='This command evaluates input. It has one argument, the input you want to evaluate.')
    async def eval(self, ctx, *, cmd):  # https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9
        """Evaluates input.
        Input is interpreted as newline seperated statements.
        If the last statement is an expression, that is the return value.
        Usable globals:
          - `bot`: the bot instance
          - `discord`: the discord module
          - `commands`: the discord.ext.commands module
          - `ctx`: the invocation context
          - `__import__`: the builtin `__import__` function
        Such that `>eval 1 + 1` gives `2` as the result.
        The following invocation will cause the bot to send the text '9'
        to the channel of invocation and return '3' as the result of evaluating
        >eval ```
        a = 1 + 2
        b = a * 2
        await ctx.send(a + b)
        a
        ```
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

    @commands.command(name='shell',
                      help='This command gives you shell access to the server. It has one argument, the command you want to run.',
                      brief='This command gives you shell access to the server.')
    async def shell(self, ctx, args=None):
        if args is None:
            await ctx.send('Please enter a command.')
        else:  # https://docs.python.org/3/library/asyncio-subprocess.html
            proc = await asyncio.create_subprocess_shell(
                args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)

            stdout, stderr = await proc.communicate()

            embed1 = discord.Embed(title='Shell', description=f'[{args!r} exited with {proc.returncode}]',
                                   color=discord.Color.green())
            embed2 = None
            embed3 = None
            if stdout:
                embed2 = discord.Embed(title='stdout', description=f'```{stdout.decode()}```',
                                       color=discord.Color.green())
            if stderr:
                embed3 = discord.Embed(title='stderr', description=f'```{stderr.decode()}```',
                                       color=discord.Color.green())
            await ctx.send(embeds=[embed1, embed2, embed3])


async def setup(bot):
    await bot.add_cog(Dev(bot))
