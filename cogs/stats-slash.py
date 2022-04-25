import aiohttp
import discord
from discord import interactions, app_commands
from discord.ext import commands

class Stats(commands.Cog, name="stats-slash"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.commands(
        name="stats",
        description="Check statistics of the bot.",
    )
    async def stats(self, interaction: interactions) -> None:
        """
        Check if the bot is alive.
        :param interaction: The application command interaction.
        """
        view = discord.ui.View()
        item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Invite Me", url="https://discord.com/api/oauth2/authorize?client_id=872002294219157534&permissions=8&scope=bot%20applications.commands")
        item1 = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Community Server", url="https://discord.gg/YjPUyP4q2J")
        item2 = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Documentation", url="https://discord.gg/YjPUyP4q2J")
        view.add_item(item=item)
        view.add_item(item=item1)
        view.add_item(item=item2)
        servers = len(self.bot.guilds)
        members = 0
        for guild in self.bot.guilds:
            members += guild.member_count - 1
        embed = discord.Embed(
            title=f"Bot Statistics",
            description = f"__**Developers**__\n・[varchasvkhare#6684](https://discordapp.com/users/868465221373665351)\n\n__**Presence**__\n・Latency - {str(round(self.bot.latency * 1000))}ms\n・Shard - {interaction.guild.shard_id}\n・Servers - {servers}\n・Users - {members}",
            color=0x9C84EF
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/872701275685404713/959730230157778974/959729564957958204.webp')
        await interaction.send(embed=embed, ephemeral = True, view = view)


async def setup(bot):
    await bot.add_cog(Stats(bot))