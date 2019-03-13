from discord.ext.commands import Cog, command, Context, is_owner
from discord import Embed, Member
from aiohttp import ClientSession
from .common import invalid_arg
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
        em.set_image(
            url=f"https://amadeus.jacobjaeger.net/gifs/hugging/{randint(0, ctx.bot.gif_sizes['hugging'] - 1)}.gif")
        await ctx.send(embed=em)

    @command("kiss", help="kiss someone or get kissed")
    async def kiss(self, ctx: Context, user: Optional[Member] = None):
        if user:
            title = f"{user.mention} got kissed by {ctx.author.mention}"
        else:
            title = f"{ctx.author.mention} got kissed"
        em = Embed(description=title, color=0xFF00AA)
        em.set_image(
            url=f"https://amadeus.jacobjaeger.net/gifs/kissing/{randint(0, ctx.bot.gif_sizes['kissing'] - 1)}.gif")
        await ctx.send(embed=em)





def setup(bot):
    bot.add_cog(Roleplay())
