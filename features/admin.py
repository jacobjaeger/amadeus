from discord.ext.commands import Cog, command, Context, Bot
from discord import Embed, Member
from aiohttp import ClientSession
from .common import invalid_arg, perms_or_sudo
from random import choice
from typing import Optional


class Admin(Cog):
    @command("purge", help="purge the last n (arg) messages from the current channel")
    @perms_or_sudo('manage_messages')
    async def purge(self, ctx: Context, n: Optional[int] = 100):
        await ctx.channel.purge(limit=n + 1)

    @command("ban", help="ban someone")
    @perms_or_sudo('ban_members')
    async def ban(self, ctx: Context, member: Member, *, reason: Optional[str] = None):
        if not await ctx.bot.is_owner(member):
            await member.ban(reason=reason)
        em = Embed(
            title="ban successfull",
            description=f"**{member.display_name}** has been banned",
            color=0xFF0000
        )
        em.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Admin())
