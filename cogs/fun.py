import random
import asyncio

import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.group(name='truth', invoke_without_command=True, aliases=['t'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def truth(self, ctx):
        embed = discord.Embed(
            title = "Truth", description = f"{random.choice(self.bot.fun_database['truths'])}"
        ).set_thumbnail(
            url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
        )
        await ctx.send(embed=embed)

    @truth.command(name='nsfw', aliases=['n'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.is_nsfw()
    async def nsfw_truth(self, ctx):
        embed = discord.Embed(
            title = "Truth <:18:917826933209829466>", description = f"{random.choice(self.bot.fun_database['nsfw_truth'])}"
        ).set_thumbnail(
            url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.member)
    async def gtn(self, ctx):
        number = random.randint(1, 100)
        await ctx.send('Guess a number between 1 to 100!')

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author and m.content.isdigit()

        for i in range(0, 5):        
            try:
                message = await self.bot.wait_for(
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
        
    @commands.group(name='dare', invoke_without_command=True, aliases=['d'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def dare(self, ctx):
        embed = discord.Embed(
            title = "Dare", description = f"{random.choice(self.bot.fun_database['dares'])}"
        ).set_thumbnail(
            url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
        )
        await ctx.send(embed=embed)

    @dare.command(name='nsfw', aliases=['n'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.is_nsfw()
    async def nsfw_dare(self, ctx):
        embed = discord.Embed(
            title = "Dare <:18:917826933209829466>", description = f"{random.choice(self.bot.fun_database['nsfw_dare'])}"
        ).set_thumbnail(
            url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024'
        )
        await ctx.send(embed=embed)

    @commands.command(name='never', aliases=['neverhaveiever', 'nhie', 'ever', 'n'])
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def never(self, ctx):
        embed = discord.Embed(title = "Never Have I Ever", description = f"{random.choice(self.bot.fun_database['nhie'])}")
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/871986650157297685/204c06ac6be9d5f85f36f5b103581489.png?size=1024')
        await ctx.reply(embed=embed)

    @commands.command(aliases = ['tot', 'tt'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def thisorthat(self, ctx):
        """Get a this or that question."""

        response = random.choice(self.bot.fun_database['tot'])
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
    
async def setup(bot):
    bot.add_cog(Fun(bot))