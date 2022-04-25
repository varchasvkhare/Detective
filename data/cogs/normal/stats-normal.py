import discord
from discord.ext import commands
from discord.ext.commands import Context

class Stats(commands.Cog, name="stats-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="stats", aliases = ["statistics", "ping", "botinfo"],
        description="Check information about the bot.",
    )
    async def stats(self, context: Context) -> None:
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
            description = f"__**Developers**__\n・[varchasvkhare#6684](https://discordapp.com/users/868465221373665351)\n[invalid-user#1119](https://discordapp.com/users/714731543309844561)\n\n__**Presence**__\n・Latency - {str(round(self.bot.latency * 1000))}ms\n・Shard - {context.guild.shard_id}\n・Servers - {servers}\n・Users - {members}",
            color=0x9C84EF
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/872701275685404713/959730230157778974/959729564957958204.webp')
        await context.send(embed=embed,view = view)
        
def setup(bot):
    bot.add_cog(Stats(bot))