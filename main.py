import random
import os
import traceback
import sys
import asyncio
import inspect

import discord
from discord.ext import commands, tasks, menus
import asyncpg

class BetterHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                'name': 'help',
                'help': 'Shows the help command for Detective bot.'
            }
        )

BOT_TOKEN = 'ODcxNjk3MTgwMDQwMjUzNDgx.YQfFQw.vJLVpVsQKuKv8OsfMQdDVzqbcqs'
POSTGRES_DSN = 'postgres://xmlluvrkcwnoxn:7b5307728139ba19c8c4990f658ad9a2945d34e1893f22142d9441813f091ebf@ec2-3-218-171-44.compute-1.amazonaws.com:5432/d3tgnrh10m69n'

async def get_prefix(bot: commands.Bot, message: discord.Message):
    prefix = await bot.db.fetchval('SELECT prefix FROM prefixes WHERE guild_id = $1', message.guild.id)
    
    prefix = prefix or 'd/' # default pre

    return prefix

bot = commands.AutoShardedBot(
    command_prefix=get_prefix,
    shard_count=1, 
    intents=discord.Intents.all(),
    case_insensitive=True,
    strip_after_prefix=True,
    help_command=BetterHelp(),
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

bot.fun_database = {
    "truths": parse_list_file('data/truths.txt'),
    "dares": parse_list_file('data/dares.txt'),
    "nhie": parse_list_file('data/nhie.txt'),
    "nsfw_truth": parse_list_file('data/nsfw_truth.txt'),
    "nsfw_dare": parse_list_file('data/nsfw_dare.txt'),
    "tot": parse_list_file('data/tot.txt')
}

@bot.check
async def blacklisted_check(ctx: commands.Context):
    # bot owners bypass this
    if await bot.is_owner(ctx.author):
        return True

    res = await bot.db.fetchval('SELECT user_id FROM blacklist WHERE user_id = $1', ctx.author.id)
    if res: # db contains an entry - blacklisted so return False (cant use bot)
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
    else: # everything is normal, not blacklisted
        return True

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

    extensions = [
        'jishaku',
        *[
            f'cogs.{extension[:-3]}'
            for extension in os.listdir('./cogs')
            if extension.endswith('.py')
        ]
    ]

    for item in extensions:
        try:
            await bot.load_extension(item)
        except Exception as exc:
            print(f"Failed to load extension {item}", exc_info=exc)
            traceback.print_exc()

    bot.db = await asyncpg.create_pool(dsn=POSTGRES_DSN)

    change_status.start()

bot.run(BOT_TOKEN)