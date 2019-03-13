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


def setup(bot):
    bot.add_cog(NSFW())
