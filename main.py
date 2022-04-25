import random
import json
import os
import io
import textwrap
import re
import traceback

import discord
from discord.ext import commands, tasks
import import_expression


async def get_prefix(bot: commands.Bot, message: discord.Message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.AutoShardedBot(
    command_prefix=get_prefix,
    shard_count=1, 
    intents=discord.Intents.all(),
    case_insensitive=True,
    help_command=commands.DefaultHelpCommand(),
    owner_ids=[
        868465221373665351,
        714731543309844561 # invalid
    ]
)
bot._last_result = None # for eval cmd

@tasks.loop(minutes=1)
async def change_status():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=f'd/help | {str(len(bot.guilds))} servers'
        )
    )

@change_status.before_loop
async def _before_change_status():
    await bot.wait_until_ready()

@bot.event
async def on_ready():
    print(f'Logged in {bot.user} (ID: {bot.user.id})')
    print('------')
    change_status.start()

    await bot.load_extension('jishaku')

@bot.listen('on_guild_join')
async def guild_join_handler(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = 'd/'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.listen('on_guild_remove')
async def guild_remove_handler(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.command(name='eval')
@commands.is_owner()
async def _eval(self, ctx: commands.Context, *, body: str):
    """Evaluates a code"""

    env = {
        'bot': bot,
        '_b': bot,
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
        '_': bot._last_result,
        '_get': discord.utils.get,
        '_find': discord.utils.find,
    }

    env.update(globals())

    def cleanup_code(content: str) -> str:
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        _regex = re.compile(r"^((```py(thon)?)(?=\s)|(```))")
        if content.startswith('```') and content.endswith('```'):
            return _regex.sub("", content)[:-3]

        # remove `foo`
        return content.strip('` \n')

    body = cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with import_expression.redirect_stdout(stdout):
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

bot.run('ODcxNjk3MTgwMDQwMjUzNDgx.YQfFQw.vJLVpVsQKuKv8OsfMQdDVzqbcqs')