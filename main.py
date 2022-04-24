import discord
from discord.ext import commands
import random
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

def get_prefix(client, message):
    with open('prefix.json', 'r') as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]

bot = commands.AutoShardedBot(shard_count=1, command_prefix=(get_prefix), intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Activity(name=(f'd/help | {str(len(bot.guilds))} servers'), type=discord.ActivityType.playing))

@bot.event
async def on_guild_join(guild):
    with open('prefix.json', 'r') as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = 'd/'

    with open('prefix.json', 'w') as f:
        json.dump(prefix, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefix.json', 'r') as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

    with open('prefix.json', 'w') as f:
        json.dump(prefix, f, indent=4)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined in {member.joined_at}')

bot.run('ODcxNjk3MTgwMDQwMjUzNDgx.YQfFQw.vJLVpVsQKuKv8OsfMQdDVzqbcqs')