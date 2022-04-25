import random
import json
import os
import io
import textwrap
import re
import traceback
import sys
import asyncio
import inspect

import discord
from discord.ext import commands, tasks, menus
import import_expression

class BetterHelp(HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                'name': 'help',
                'help': 'Shows the help command for Detective bot.'
            }
        )

BOT_TOKEN = 'ODcxNjk3MTgwMDQwMjUzNDgx.YQfFQw.vJLVpVsQKuKv8OsfMQdDVzqbcqs'

async def get_prefix(bot: commands.Bot, message: discord.Message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.AutoShardedBot(
    command_prefix=get_prefix,
    shard_count=1, 
    intents=discord.Intents.all(),
    case_insensitive=True,
    help_command=commands.BetterHelp(),
    owner_ids=[
        868465221373665351,
        714731543309844561 # invalid
    ]
)

# setup

def parse_list_file(file_path: str) -> list:
	"""Parse a text file into a list containing each line."""
	
	with open(file_path) as f:
		return [l.strip() for l in f.readlines() if l.strip()]

database = {
    "truths": parse_list_file('data/truths.txt'),
    "dares": parse_list_file('data/dares.txt'),
    "nhie": parse_list_file('data/nhie.txt'),
    "nsfw_truth": parse_list_file('data/nsfw_truth.txt'),
    "nsfw_dare": parse_list_file('data/nsfw_dare.txt'),
    "tot": parse_list_file('data/tot.txt')
}

with open("blacklist.json", "r") as f:
    blacklist = json.load(f)

with open("n-rating-guild.json", "r") as f:
    nrating = json.load(f)

# main cmds

@bot.command()
async def ping(ctx):
    embedVar = discord.Embed(title="Latency", description=f"<a:latency:871646202389737483> {str(round(bot.latency * 1000))}ms\nShard {ctx.guild.shard_id}")
    await ctx.send(embed=embedVar)

@bot.command(name='report')
@commands.cooldown(1, 60, commands.BucketType.user)
async def report(ctx, user: discord.User, *, reason: str):
    channel = bot.get_channel(892680687973433354)
    embed = discord.Embed(description = f"Offender ID - {user.id}\nReported by - {ctx.author.id}\nReason - {reason}", color = 0xFFF59E)
    await channel.send(embed = embed)
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.mention} - *Thanks for the report, it has been sent to bot staff!*")

@bot.command()
async def servers(ctx):
    embed = discord.Embed(description=f"I am in {len(bot.guilds)} servers!", colour=0xFFF59E)
    await ctx.send(embed=embed)

@bot.group(name='truth', invoke_without_command=True, aliases=['t'])
@commands.cooldown(1, 3, commands.BucketType.member)
async def truth(ctx):
    embed = discord.Embed(
        title = "Truth", description = f"{random.choice(database['truths'])}"
    ).set_thumbnail(
        url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
    )
    await ctx.send(embed=embed)

@truth.command(name='nsfw', aliases=['n'])
@commands.cooldown(1, 3, commands.BucketType.member)
@commands.is_nsfw()
async def nsfw_truth(ctx):
    embed = discord.Embed(
        title = "Truth <:18:917826933209829466>", description = f"{random.choice(database['nsfw_truth'])}"
    ).set_thumbnail(
        url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.max_concurrency(1, commands.BucketType.member)
async def gtn(ctx):
    number = random.randint(1, 100)
    await ctx.send('Guess a number between 1 to 100!')

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author and m.content.isdigit()

    for i in range(0, 5):        
        try:
            message = await bot.wait_for(
                'message', 
                timeout=15.0, 
                check=check
            )
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} - The guess the number session has timed out!")
            break
        
        guess = int(message.content)
        if guess > number:
            await ctx.reply('Guess a smaller number!')
        elif guess < number:
            await ctx.reply('Guess a larger number!')
        else:
            await ctx.reply(f'Congrats, you have won the game! The number was **{number}**.')
            break
    
@bot.group(name='dare', invoke_without_command=True, aliases=['d'])
@commands.cooldown(1, 3, commands.BucketType.member)
async def dare(ctx):
    embed = discord.Embed(
        title = "Dare", description = f"{random.choice(database['dares'])}"
    ).set_thumbnail(
        url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
    )
    await ctx.send(embed=embed)

@dare.command(name='nsfw', aliases=['n'])
@commands.cooldown(1, 3, commands.BucketType.member)
@commands.is_nwfw()
async def nsfw_dare(ctx):
    embed = discord.Embed(
        title = "Dare <:18:917826933209829466>", description = f"{random.choice(database['nsfw_dare'])}"
    ).set_thumbnail(
        url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
    )
    await ctx.send(embed=embed)

@bot.command(name='never', aliases=['neverhaveiever', 'nhie', 'ever', 'n'])
@commands.cooldown(1, 3, commands.BucketType.member)
async def never(ctx):
    embed = discord.Embed(title = "Never Have I Ever", description = f"{random.choice(database['nhie'])}")
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024')
    await ctx.reply(embed=embed)

@bot.command(aliases = ['tot', 'tt'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def thisorthat(ctx):
    """Get a this or that question."""

    response = random.choice(database['tot'])
    message = []

    if ':' in response: 
        split = response.split(':')
        message.append(f"**{split[0]}**")
        tort = split[1].strip()
    else:
        tort = response
    
    message.append(f"🔴 {tort.replace(' or ', ' **OR** ')} 🔵")

    embed = discord.Embed(
        description='\n'.join(message)
    )
    sent_embed = await ctx.send(embed = embed)
    await sent_embed.add_reaction("🔴")
    await sent_embed.add_reaction("🔵")

@bot.command() # hm ok then
async def community(ctx):
    view = discord.ui.View()
    button = discord.ui.Button(
        label='Join the community server!',
        url='https://discord.gg/YjPUyP4q2J'
    )
    view.add_item(button)

    embed = discord.Embed(
        title = "• ━━ V A N Q U I S H E R ━━ •",
        description=inspect.cleandoc(
            """> ***Events!!***
            ・:detective: mafia, :crossed_swords: rumble, :tea: tea, :notes: music and more!
            > ***Robbing is disabled!!***
            ・:moneybag: don't worry about being robbed
            > ***Giveaways!!***
            ・:frog: dank, :purse: mafia points, :pound: owo and more!
            > ***Welcoming community!!***
            ・make friends and have fun, we're sfw!
            > ***Extras!!***
            ・weekly giveaways and gaming events.
            ・lots of enjoyment and fun.
            ・so many bots to use and even custom bots.
            ・a ton of perks.
            ──────────────────────────────────────────────
            **Join us NOW and become part of an amazing, growing and welcoming community.**
            ──────────────────────────────────────────────"""
        )
    )
    await ctx.reply(embed=embed, view=view)

# events

@bot.listen('on_command_error')
async def error_handler(ctx, error):
    embed = discord.Embed(
        colour=0xff0000
    )
    
    if isinstance(error, commands.MissingRequiredArgument):
        embed.description = str(error)[:4096]
        return await ctx.reply(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        if await bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
            return await ctx.reinvoke()

        embed.title = "Slow it down bro!"
        embed.description = f"Try again in {error.retry_after:.2f}s."
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.NotOwner):
        embed.description = "Only my owners can use this command!"
        return await ctx.reply(embed=embed)
    elif isinstance(error, commands.NSFWChannelRequired):
        embed.description = "This command can only be used in a NSFW channel."
        return await ctx.reply(embed=embed)
    elif isinstance(error, (commands.BadArgument, commands.BadBoolArgument, commands.BadUnionArgument, commands.BadColourArgument, commands.BadInviteArgument)):
        embed.description = str(error)[:4096]
        return await ctx.reply(embed=embed)
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        embed.description = str(error)[:4096]
        await ctx.reply(embed=embed)

@bot.check
async def blacklisted_check(ctx: commands.Context):
    if ctx.author.id in blacklist:
        delete_after: int = 7
        
        embed = discord.Embed(
            description='Unfortunately, you have been blacklisted from the bot. If you wish to know why or appeal, please join **[this server](https://discord.gg/xRquATkezz)**.'
        )
        await ctx.reply(
            embed=embed,
            delete_after=delete_after
        )
        await ctx.message.delete(delay=delete_after)

        return False
    return True

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
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
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

# owner cmds

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


#custom prefix
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')



bot.run(BOT_TOKEN)