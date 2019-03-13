from discord.ext.commands import Cog, command, Context, is_nsfw
from discord import Embed
from aiohttp import ClientSession
from .common import invalid_arg, get_nekos_life
from random import choice


class NSFW(Cog):
    @command("trap", help="traps aren't gay")
    @is_nsfw()
    async def trap(self, ctx: Context):
        em = Embed(title="traps aren't gay", color=0xFF00AA)
        em.set_image(url=await get_nekos_life("trap"))
        await ctx.send(embed=em)

    @command("nsfwneko", help="traps aren't gay")
    @is_nsfw()
    async def neko(self, ctx: Context):
        em = Embed(title="traps aren't gay", color=0xFF00AA)
        em.set_image(url=await get_nekos_life("trap"))
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(NSFW())
