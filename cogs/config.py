import discord
from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def prefix(self, ctx, new_prefix: str):
        old_prefix = await self.bot.db.fetchval('SELECT prefix FROM prefixes WHERE guild_id = $1', ctx.guild.id)

        if not old_prefix:
            await self.bot.db.execute('INSERT INTO prefixes VALUES($1, $2)', ctx.guild.id, new_prefix)
        else:
            await self.bot.db.execute('UPDATE prefixes SET prefix = $1 WHERE guild_id = $2', new_prefix, ctx.guild.id)

        await ctx.send(f'Prefix set to: {new_prefix}', allowed_mentions=discord.AllowedMentions().none())

async def setup(bot):
    await bot.add_cog(Config(bot))