from discord.ext.commands import Cog, command, Context, is_owner
from discord import Embed
from aiohttp import ClientSession
from .common import invalid_arg
from random import choice


class Owner(Cog):
    hidden = True

    @command("sudo", hidden=True)
    @is_owner()
    async def sudo(self, ctx: Context, state: bool):
        ctx.bot.sudo = state
        await ctx.send(embed=Embed(
            title=f"sudo {'on' if state else 'off'}",
            color=0x00FF00 if state else 0xFF0000
        ))

    @command("counter", hidden=True)
    @is_owner()
    async def counter(self, ctx: Context):
        await ctx.send(embed=Embed(
            title=str(ctx.bot.counter),
            color=0xFF00AA
        ))


def setup(bot):
    bot.add_cog(Owner())
