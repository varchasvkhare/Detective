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
        prefix = await self.bot.db.fetchval('SELECT prefix FROM prefixes WHERE guild_id = $1', ctx.guild.id)
        
        embed = discord.Embed(
            title = f"Help",
            description = inspect.cleandoc(
                f"""
                Hy, I'm {self.bot.user.name}!
                You can have a look at my commands below.
                For further help, join my [server](https://discord.gg/YjPUyP4q2J).
                Prefix for the server is `{prefix}`
                """
            )
        )
        embed.set_author(
            name = self.bot.user.name,
            icon_url = self.bot.user.avatar
        )
        embed.add_field(
            name='General',
            value = inspect.cleandoc(
                f"""
                ```
                Community
                Help
                Invite
                Ping
                Prefix
                Vote
                ```
                """
            ),
            inline=True
        )
        embed.add_field(
            name='Games',
            value = inspect.cleandoc(
                f"""
                ```
                Truth
                Date
                NeverHaveIEver
                ThisorThat
                Connect4
                ```
                """
            ),
            inline=True
        )

        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Help(bot))