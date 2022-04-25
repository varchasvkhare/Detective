import textwrap
import re
import traceback
import io
import contextlib

import discord
from discord.ext import commands
import import_expression

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def cleanup_code(self, content: str) -> str:
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        _regex = re.compile(r"^((```py(thon)?)(?=\s)|(```))")
        if content.startswith('```') and content.endswith('```'):
            return _regex.sub("", content)[:-3]

        # remove `foo`
        return content.strip('` \n')

    @commands.command(name='eval')
    @commands.is_owner()
    async def _eval(self, ctx: commands.Context, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            '_b': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            '_c': ctx.channel,
            'author': ctx.author,
            '_a': ctx.author,
            'guild': ctx.guild,
            '_g': ctx.guild,
            'message': ctx.message,
            '_m': ctx.message,
            'reference': getattr(ctx.message.reference, 'resolved', None),
            '_r': getattr(ctx.message.reference, 'resolved', None),
            '_': self._last_result,
            '_get': discord.utils.get,
            '_find': discord.utils.find,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            import_expression.exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
    
async def setup(bot):
    await bot.add_cog(Owner(bot))