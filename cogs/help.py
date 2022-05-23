import inspect
from multiprocessing.dummy.connection import Client
from typing_extensions import Self

import discord
from discord.ext import commands

from __main__ import Bot

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="help", aliases = ["h"]
    )
    async def help(self, ctx: commands.Context) -> None:
        """Help command"""

        guilds_count = len(self.bot.guilds)
        members_count = sum(g.member_count for g in self.bot.guilds)
        
        embed = discord.Embed(
            title=f"{self.bot.user.name}",
            url = self.bot.user.avatar
        )
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Help(bot))