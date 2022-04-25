import random
import json
import os

import discord
from discord.ext import commands, tasks

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.AutoShardedBot(
    command_prefix=get_prefix,
    shard_count=1, 
    intents=discord.Intents.all(),
    case_insensitive=True,
    help_command=commands.DefaultHelpCommand()
)

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

# @bot.listen('on_member_join')
# async def welcome_member(member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f'{member.name} joined in {member.joined_at}')

bot.run('ODcxNjk3MTgwMDQwMjUzNDgx.YQfFQw.vJLVpVsQKuKv8OsfMQdDVzqbcqs')