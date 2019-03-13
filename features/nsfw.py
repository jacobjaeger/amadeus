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

    @command("lewdnekogif", help="get a nsfw neko gif")
    @is_nsfw()
    async def lewdnekogif(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("nsfw_neko_gif"))
        await ctx.send(embed=em)

    @command("lewdneko", help="get a nsfw neko")
    @is_nsfw()
    async def lewdneko(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("lewd"))


def setup(bot):
    bot.add_cog(NSFW())
