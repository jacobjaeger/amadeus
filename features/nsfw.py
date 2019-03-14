from discord.ext.commands import Cog, command, Context, check
from discord import Embed, TextChannel
from aiohttp import ClientSession
from .common import invalid_arg, get_nekos_life, NSFWError
from random import choice


def is_nsfw():
    def pred(ctx):
        if not (isinstance(ctx.channel, TextChannel) and ctx.channel.is_nsfw()):
            raise NSFWError("you can't execute a nsfw command in a non-nsfw channel")
        return True
    return check(pred)


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
        await ctx.send(embed=em)

    @command("hentai", help="get a random hentai pic")
    @is_nsfw()
    async def hentai(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("hentai"))
        await ctx.send(embed=em)

    @command("femdom", help="get a random femdom hentai pic")
    @is_nsfw()
    async def femdom(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("femdom"))
        await ctx.send(embed=em)

    @command("boobs", help="get a random ecchi pic")
    @is_nsfw()
    async def boobs(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("boobs"))
        await ctx.send(embed=em)

    @command("yuri", help="get a random yuri pic")
    @is_nsfw()
    async def yuri(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("yuri"))
        await ctx.send(embed=em)

    @command("feet", help="get a random feet pic")
    @is_nsfw()
    async def feet(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("feet"))
        await ctx.send(embed=em)

    @command("kitsune", help="get a random kitsune pic")
    @is_nsfw()
    async def kitsune(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("lewdk"))
        await ctx.send(embed=em)

    @command("hentaigif", help="get a random hentai gif")
    @is_nsfw()
    async def hentaigif(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("Random_hentai_gif"))
        await ctx.send(embed=em)

    @command("anal", help="get a random anal hentai picture/gif")
    @is_nsfw()
    async def anal(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_image(url=await get_nekos_life("anal"))
        await ctx.send(embed=em)



def setup(bot):
    bot.add_cog(NSFW())
