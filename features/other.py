from discord.ext.commands import Cog, command, Context, Converter, BadArgument
from discord import Embed, Member
import discord
from aiohttp import ClientSession
from .common import invalid_arg
from random import choice, randint
from typing import Optional, Union
from re import compile


class Color(Converter):
    REGEX = compile(r"#?([A-Fa-f0-9]{2}){3}")

    async def convert(self, ctx: Context, argument):
        if not self.REGEX.match(argument):
            raise BadArgument(f"{argument} is not a valid hex color")
        argument = argument if not argument.startswith("#") else argument[1:]
        return tuple((argument[:2], argument[2:4], argument[4:]))


class Other(Cog):
    @command("color", help="show info about a color")
    async def color(self, ctx: Context, color: Color):  # noqa
        em = Embed(
            title="#" + "".join(color),
            description=f"rgb({int(color[0], base=16)}, {int(color[1], base=16)}, {int(color[2], base=16)})",
            color=int("".join(color), base=16)
        )  # noqa
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Other())
