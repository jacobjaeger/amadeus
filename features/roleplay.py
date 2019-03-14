from discord.ext.commands import Cog, command, Context, is_owner
from discord import Embed, Member
from aiohttp import ClientSession
from .common import invalid_arg, get_nekos_life
from random import randint
from typing import Optional


class Roleplay(Cog):
    @command("hug", help="hug someone or get hugged")
    async def hug(self, ctx: Context, user: Optional[Member] = None):
        if user:
            title = f"{user.mention} got hugged by {ctx.author.mention}"
        else:
            title = f"{ctx.author.mention} got hugged"
        em = Embed(description=title, color=0xFF00AA)
        em.set_image(url=await get_nekos_life("hug"))
        await ctx.send(embed=em)

    @command("kiss", help="kiss someone or get kissed")
    async def kiss(self, ctx: Context, user: Optional[Member] = None):
        if user:
            title = f"{user.mention} got kissed by {ctx.author.mention}"
        else:
            title = f"{ctx.author.mention} got kissed"
        em = Embed(description=title, color=0xFF00AA)
        em.set_image(url=await get_nekos_life("kiss"))
        await ctx.send(embed=em)

    @command("slap", help="slap someone or get slapped")
    async def slap(self, ctx: Context, user: Optional[Member] = None):
        if user:
            title = f"{user.mention} got slapped by {ctx.author.mention}"
        else:
            title = f"{ctx.author.mention} got slapped"
        em = Embed(description=title, color=0xFF00AA)
        em.set_image(url=await get_nekos_life("slap"))
        await ctx.send(embed=em)

    @command("poke", help="poke someone or get poked")
    async def poke(self, ctx: Context, user: Optional[Member] = None):
        if user:
            title = f"{user.mention} got poked by {ctx.author.mention}"
        else:
            title = f"{ctx.author.mention} got poked"
        em = Embed(description=title, color=0xFF00AA)
        em.set_image(url=await get_nekos_life("poke"))
        await ctx.send(embed=em)

    @command("pat", help="pat someone or get patted")
    async def pat(self, ctx: Context, user: Optional[Member] = None):
        if user:
            title = f"{user.mention} got patted by {ctx.author.mention}"
        else:
            title = f"{ctx.author.mention} got patted"
        em = Embed(description=title, color=0xFF00AA)
        em.set_image(url=await get_nekos_life("pat"))
        await ctx.send(embed=em)

    @command("cuddle", help="cuddle someone or get cuddled")
    async def cuddle(self, ctx: Context, user: Optional[Member] = None):
        if user:
            title = f"{user.mention} got cuddled by {ctx.author.mention}"
        else:
            title = f"{ctx.author.mention} got cuddled"
        em = Embed(description=title, color=0xFF00AA)
        em.set_image(url=await get_nekos_life("cuddle"))
        await ctx.send(embed=em)

    @command("baka", help="BAKA!!!")
    async def baka(self, ctx: Context):
        em = Embed(title="BAKA!!!", color=0xFF00AA)
        em.set_image(url=await get_nekos_life("baka"))
        await ctx.send(embed=em)

    @command("smug", help="are you feeling smug? show it with this command")
    async def smug(self, ctx: Context):
        em = Embed(description=f"{ctx.author.mention} is feeling smug", color=0xFF00AA)
        em.set_image(url=await get_nekos_life("smug"))
        await ctx.send(embed=em)

    @command("tickle", help="tickle someone or get tickled")
    async def tickle(self, ctx: Context, user: Optional[Member] = None):
        if user:
            title = f"{user.mention} got tickled by {ctx.author.mention}"
        else:
            title = f"{ctx.author.mention} got tickled"
        em = Embed(description=title, color=0xFF00AA)
        em.set_image(url=await get_nekos_life("tickle"))
        await ctx.send(embed=em)






def setup(bot):
    bot.add_cog(Roleplay())
