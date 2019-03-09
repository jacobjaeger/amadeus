from discord.ext.commands import Cog, command, Context
from discord import Embed, TextChannel
from aiohttp import ClientSession
from .common import invalid_arg, perms_or_sudo
from random import choice
from typing import Optional


class Admin(Cog):
    @command("purge", help="purge the last n (arg) messages from the current channel")
    @perms_or_sudo('manage_messages')
    async def purge(self, ctx: Context, n: Optional[int] = 100):
        await ctx.channel.purge(limit=n + 1)


def setup(bot):
    bot.add_cog(Admin())
