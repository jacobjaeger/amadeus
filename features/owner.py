from discord.ext.commands import Cog, command, Context, is_owner
from discord import Embed, Message
from aiohttp import ClientSession
from .common import invalid_arg
from random import choice
import asyncio
import async_timeout


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

    @command("sh", hidden=True)
    @is_owner()
    async def sh(self, ctx: Context, *, prog):
        msg: Message = await ctx.send(embed=Embed(
            title="executing shell command...",
            description=f"```\n$ {prog}\n```",
            color=0xFF00AA
        ))
        try:
            async with async_timeout.timeout(30) as cm:
                proc = await asyncio.create_subprocess_shell(prog, stdout=asyncio.subprocess.PIPE,
                                                             stderr=asyncio.subprocess.PIPE)
                stdout, stderr = await proc.communicate()
                NEWLINE = "\n"
                body = f"```$ {prog}\n\n{str(stdout, encoding='utf-8')}\n{NEWLINE + '[stderr]' + NEWLINE + str(stderr, encoding='utf-8') + NEWLINE if stderr else ''}\n[exit code {proc.returncode}]```"
        except asyncio.TimeoutError:
            body = f"```$ {prog}\n\n[process timed out]```"
        newem = Embed(
            title="executed shell command",
            description=body if len(body) <= 2048 else f"```$ {prog}\n\noutput too long...\n\n[exit code {proc.returncode}]```",
            color=0xFF0000 if proc.returncode or cm.expired else 0x00FF00
        )
        await msg.edit(embed=newem)


def setup(bot):
    bot.add_cog(Owner())
