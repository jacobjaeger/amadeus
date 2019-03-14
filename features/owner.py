from discord.ext.commands import Cog, command, Context, is_owner
from discord import Embed, Message
from aiohttp import ClientSession
from .common import invalid_arg
from random import choice
from sys import argv, stdout, stderr
from os import execvp
import asyncio
import async_timeout
import subprocess


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

    @command("sql", hidden=True)
    @is_owner()
    async def sql(self, ctx: Context, *, query):
        msg: Message = await ctx.send(embed=Embed(
            title="querying database...",
            description=f"```$ {query}```",
            color=0xFF00AA
        ))
        async with ctx.bot.db.execute(query) as c:
            rawres = await c.fetchall()
            rstr = ""
            for i in rawres:
                rstr += str(i)[1:-1] + "\n"
        if len(rstr) >= 2044 - len(query):
            rstr = rstr[:-(len(query) + 7)] + "..."
        await msg.edit(embed=Embed(
            title="queried database",
            description=f"```$ {query}\n\n{rstr}```",
            color=0x00FF00
        ))

    @command("quarantine", hidden=True)
    @is_owner()
    async def quarantine(self, ctx: Context):
        ctx.bot.bot_active = False
        await ctx.send(embed=Embed(
            title="bot quarantined",
            description="the bot will ignore all messages",
            color=0xFF0000
        ))

    @command("update", hidden=True)
    @is_owner()
    async def update(self, ctx: Context):
        msg = await ctx.send(embed=Embed(
            title="updating bot...",
            description="deactivating message handler",
            color=0xFF00AA
        ))
        ctx.bot.bot_active = False
        await msg.edit(embed=Embed(
            title="updating bot...",
            description="downloading updates",
            color=0xFF00AA
        ))
        proc = await asyncio.create_subprocess_shell("git pull", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if proc.returncode:
            await msg.edit(embed=Embed(
                title="updating bot...", description="failed to update", color=0xFF0000)
            )
            ctx.bot.bot_active = True
            return
        await msg.edit(embed=Embed(
            title="updating bot...",
            description="restarting bot",
            color=0x00FF00
        ))
        try:
            ctx.bot.loop.run_until_complete(ctx.bot.logout())
        except:
            pass
        try:
            ctx.bot.loop.run_until_complete(ctx.bot.close())
        except:
            pass
        await ctx.bot.db.commit()
        await ctx.bot.db.__aexit__(None, None, None)
        execvp("python3.6", ["python3.6", *argv])


def setup(bot):
    bot.add_cog(Owner())
