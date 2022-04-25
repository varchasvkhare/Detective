import inspect

import discord
from discord import app_commands 
from discord import commands


class StatsSlash(commands.Cog, name="stats-slash"):
    def __init__(self, bot):
        self.bot = bot
        tree = app_commands.CommandTree(self.bot)
        @tree.slash_command(
        name="stats",
        description="Check statistics of the bot.",
        )
        async def stats(self, interaction: discord.interaction) -> None:
            view = discord.ui.View()
            item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Invite Me", url="https://discord.com/api/oauth2/authorize?client_id=872002294219157534&permissions=8&scope=bot%20applications.commands")
            item1 = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Community Server", url="https://discord.gg/YjPUyP4q2J")
            item2 = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Documentation", url="https://discord.gg/YjPUyP4q2J")
            view.add_item(item=item)
            view.add_item(item=item1)
            view.add_item(item=item2)
            guilds_count = len(self.bot.guilds)
            members_count = sum(g.member_count for g in self.bot.guilds)
            members = 0
            for guild in self.bot.guilds:
                members += guild.member_count - 1
            embed = discord.Embed(
                title=f"Bot Statistics",
                description = inspect.cleandoc(
                    f"""__**Developers**__
                    ・[varchasvkhare#6684](https://discordapp.com/users/868465221373665351)
                    ・[invalid-user#1119](https://discordapp.com/users/714731543309844561)
    
                    __**Presence**__
                    ・Latency - {str(round(self.bot.latency * 1000))}ms
                    ・Shard - {interaction.guild.shard_id}
                    ・Servers - {guilds_count}
                    ・Users - {members_count}
                    """
                ),
                color=0x9C84EF
            ).set_thumbnail(
                url='https://cdn.discordapp.com/attachments/870608893334659106/968156284845178901/959729564957958204.png'
            )
            await interaction.send(embed=embed, ephemeral = True, view = view)


async def setup(bot):
    await bot.add_cog(StatsSlash(bot))