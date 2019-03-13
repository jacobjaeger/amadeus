from discord.ext.commands import Cog, command, Context, Bot, BadArgument
from discord import Embed, Member
from aiohttp import ClientSession
from .common import invalid_arg, perms_or_sudo
from random import choice
from typing import Optional, Union


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

    @command("kick", help="kick someone")
    @perms_or_sudo('kick_members')
    async def kick(self, ctx: Context, member: Member, *, reason: Optional[str] = None):
        if not await ctx.bot.is_owner(member):
            await member.kick(reason=reason)
        em = Embed(
            title="kick successfull",
            description=f"**{member.display_name}** has been kicked",
            color=0xFF0000
        )
        em.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=em)

    @command("config", help="configure server-wide settings for the bot", requires_server_db=True)
    @perms_or_sudo('manage_server')
    async def config(self, ctx: Context, key: Optional[str] = None, value: Optional[str] = None):
        if value is None:
            pass
        elif value.lower() in ("yes", "y", "on", "t", "true"):
            value = True
        elif value.lower() in ("no", "n", "off", "f", "false"):
            value = False
        else:
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    raise BadArgument()
        if key is None:
            await ctx.send(embed=Embed(
                title="here is a list of all the set config keys on this server",
                description="\r\n".join([f"`{i}` -> `{str(ctx.conf[i]).lower()}`" for i in ctx.bot.default_config]),
                color=0xFF00AA
            ))
        elif value is None:
            if key in ctx.bot.default_config:
                await ctx.send(embed=Embed(
                    title=f"the value for config key `{key}`",
                    description=f"is `{str(ctx.conf[key]).lower()}`",
                    color=0xFF00AA
                ))
            else:
                await ctx.send(embed=Embed(
                    title="invalid config key",
                    description=f"the config key `{key}` does not exist",
                    color=0xFF0000
                ))
        else:
            if key in ctx.bot.default_config:
                if type(value) != type(ctx.bot.default_config[key]):
                    await ctx.send(embed=Embed(
                        title="invalid value type",
                        description=f"couldn't set `{key}`",
                        color=0xFF0000
                    ))
                    return
                ctx.conf[key] = value
                await ctx.send(embed=Embed(
                    title=f"config value `{key}`",
                    description=f"has been set to `{str(value).lower()}`",
                    color=0x00FF00
                ))
            else:
                await ctx.send(embed=Embed(
                    title="invalid config key",
                    description=f"the config key `{key}` does not exist",
                    color=0xFF0000
                ))


def setup(bot):
    bot.add_cog(Admin())
