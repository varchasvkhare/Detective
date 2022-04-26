import random
import asyncio

import discord
from discord.ext import commands

from data import (
    dares, nsfw_dares, 
    truths, nsfw_truths, 
    neverhaveiever, 
    thisorthat
)

class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        self.fun_data = {
            'dares': dares,
            'nsfw_dares': nsfw_dares,
            'truths': truths,
            'nsfw_truths': nsfw_truths,
            'neverhaveiever': neverhaveiever,
            'thisorthat': thisorthat
        }

    @commands.group(name='truth', invoke_without_command=True, aliases=['t'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def truth(self, ctx):
        embed = discord.Embed(
            title = "Truth", description = f"{random.choice(self.fun_data['truths'])}"
        ).set_thumbnail(
            url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
        )
        await ctx.send(embed=embed)

    @truth.command(name='nsfw', aliases=['n'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.is_nsfw()
    async def nsfw_truth(self, ctx):
        embed = discord.Embed(
            title = "Truth <:18:917826933209829466>", description = f"{random.choice(self.fun_data['nsfw_truths'])}"
        ).set_thumbnail(
            url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
        )
        await ctx.send(embed=embed)
        
    @commands.group(name='dare', invoke_without_command=True, aliases=['d'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def dare(self, ctx):
        embed = discord.Embed(
            title = "Dare", description = f"{random.choice(self.fun_data['dares'])}"
        ).set_thumbnail(
            url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
        )
        await ctx.send(embed=embed)

    @dare.command(name='nsfw', aliases=['n'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.is_nsfw()
    async def nsfw_dare(self, ctx):
        embed = discord.Embed(
            title = "Dare <:18:917826933209829466>", description = f"{random.choice(self.fun_data['nsfw_dares'])}"
        ).set_thumbnail(
            url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
        )
        await ctx.send(embed=embed)

    @commands.command(name='never', aliases=['neverhaveiever', 'nhie', 'ever', 'n'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def never(self, ctx):
        embed = discord.Embed(title = "Never Have I Ever", description = f"{random.choice(self.fun_data['neverhaveiever'])}")
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024')
        await ctx.reply(embed=embed)

    @commands.command(aliases = ['tot', 'tt'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def thisorthat(self, ctx):
        """Get a this or that question."""

        response = random.choice(self.fun_data['thisorthat'])

        embed = discord.Embed()

        message = []

        if ':' in response: 
            split = response.split(':')
            embed.title = split[0]
            tot = split[1].strip()
        else:
            tot = response
        
        embed.description = (
            f"🔴 {tot.replace(' or ', ' **OR** ')} 🔵"
        )

        message = await ctx.send(embed=embed)
        await message.add_reaction("🔴")
        await message.add_reaction("🔵")

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.member)
    async def gtn(self, ctx):
        number = random.randint(1, 100)
        await ctx.send('Guess a number between 1 to 100!')

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author and m.content.isdigit()

        view = discord.ui.View()

        maximum_tries = 5
        for i in range(maximum_tries):
            view.clear_items()

            # max tries
            if i == maximum_tries:
                view.add_item(
                    discord.ui.Button(
                        label=f'{i}/{maximum_tries} tries',
                        disabled=True
                    )
                )
                await ctx.send(f"{ctx.author.mention} - Maximum tries reached! Please try again.", view=view)

            # wait for
            try:
                message = await self.bot.wait_for(
                    'message', 
                    timeout=15.0, 
                    check=check
                )
            except asyncio.TimeoutError:
                view.add_item(
                    discord.ui.Button(
                        label=f'{i}/{maximum_tries} tries',
                        disabled=True
                    )
                )
                await ctx.send(f"{ctx.author.mention} - The guess the number session has timed out!", view=view)
                break
            
            guess = int(message.content)

            if guess == number:
                view.add_item(
                    discord.ui.Button(
                        label=f'{i}/{maximum_tries} tries',
                        disabled=True
                    )
                )
                await message.reply(f'Congrats, you have won the game! The number was **{number}**.', view=view)
                break
            if guess > number:
                view.add_item(
                    discord.ui.Button(
                        label=f'{maximum_tries - i}/{maximum_tries} tries left',
                        disabled=True
                    )
                )
                await message.reply('Guess a smaller number!', view=view)
            elif guess < number:
                view.add_item(
                    discord.ui.Button(
                        label=f'{maximum_tries - i}/{maximum_tries} tries left',
                        disabled=True
                    )
                )
                await message.reply('Guess a larger number!', view=view)
    
async def setup(bot):
    await bot.add_cog(Fun(bot))