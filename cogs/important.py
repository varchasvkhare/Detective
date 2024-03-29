import inspect

import discord
from discord.ext import commands

class Important(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="stats", aliases = ["statistics", "ping", "botinfo"]
    )
    async def stats(self, ctx: commands.Context) -> None:
        """Check information about the bot."""

        view = discord.ui.View()

        invite = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Invite Me", url="https://discord.com/api/oauth2/authorize?client_id=872002294219157534&permissions=8&scope=bot%20applications.commands")
        community = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Community Server", url="https://discord.gg/YjPUyP4q2J")
        documentation = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Documentation", url="https://discord.gg/YjPUyP4q2J")

        view.add_item(invite)
        view.add_item(community)
        view.add_item(documentation)

        guilds_count = len(self.bot.guilds)
        members_count = sum(g.member_count for g in self.bot.guilds)
        
        embed = discord.Embed(
            title=f"Bot Statistics",
            description = inspect.cleandoc(
                f"""__**Developers**__
                ・[varchasvkhare#6684](https://discordapp.com/users/868465221373665351)
                ・[invalid-user#1119](https://discordapp.com/users/714731543309844561)

                __**Presence**__
                ・Latency - {str(round(self.bot.latency * 1000))}ms
                ・Shard - {ctx.guild.shard_id}
                ・Servers - {guilds_count}
                ・Users - {members_count}
                """
            ),
            color=0x9C84EF
        ).set_thumbnail(
            url='https://cdn.discordapp.com/attachments/870608893334659106/968156284845178901/959729564957958204.png'
        )
        await ctx.send(embed=embed, view=view)

    @commands.command(name='report')
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def report(self, ctx, user: discord.User, *, reason: str):
        channel = self.bot.get_channel(892680687973433354)
        embed = discord.Embed(description = f"Offender ID - {user.id}\nReported by - {ctx.author.id}\nReason - {reason}", color = 0xFFF59E)
        await channel.send(embed = embed)
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention} - *Thanks for the report, it has been sent to bot staff!*")

    @commands.command()
    async def community(self, ctx):
        view = discord.ui.View()
        button = discord.ui.Button(
            label='Join the community server!',
            url='https://discord.gg/YjPUyP4q2J'
        )
        view.add_item(button)

        embed = discord.Embed(
            title = "• ━━ D E T E C T I V E   H U B ━━ •",
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
        
async def setup(bot):
    await bot.add_cog(Important(bot))