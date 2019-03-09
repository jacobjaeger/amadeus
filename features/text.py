from discord.ext.commands import Cog, command, Context
from discord import Embed
from aiohttp import ClientSession
from .common import invalid_arg
from random import choice, randint
from typing import Optional


class Text(Cog):
    @command("reverse", help="reverses the supplied text")
    async def reverse(self, ctx: Context, *, text):
        await ctx.send(embed=Embed(
            title=f"reversed of '{text if len(text) < 15 else text[:15] + '...'}'",
            description=text[::-1],
            color=0xFF00AA
        ))

    @command("vaporwave", help="vaporwave version the supplied text")
    async def vaporwave(self, ctx: Context, *, text):
        await ctx.send(embed=Embed(
            title=f"v a p o r w a v e of '{text if len(text) < 15 else text[:15] + '...'}'",
            description=" ".join(list(text)),
            color=0xFF00AA
        ))

    @command("chucknorris", help="tells a random chuck norris joke")
    async def chucknorris(self, ctx: Context):
        async with ClientSession() as session:
            async with session.get("http://api.icndb.com/jokes/random") as resp:
                js = await resp.json()
                em = Embed(title=js["value"]["joke"].replace("&quot;", "\""),
                           color=0xFF00AA)
                em.set_footer(text="icndb.com (ID {})".format(str(js["value"]["id"])))
                await ctx.send(embed=em)

    @command("8ball", help="asks the magic 8-ball a (optional) question")
    async def eball(self, ctx: Context, *, question: Optional[str] = None):
        await ctx.send(embed=Embed(
            title=question if question is not None else "what does the magic 8-ball say?",
            description="the magic 8-ball says: " + choice([
                "yes", "totally", "definitely", "absolutely", "unquestionably",
                "i'm pretty sure", "with great certainty", "probably", "likely",
                "unsure", "i cannot say",
                "probably not", "very unlikely", "unlikely",
                "no", "definitely not", "nope"
            ]),  # todo expre -> var
            color=0xFF00AA)
        )

    @command("dice", help="roll a dice")
    async def dice(self, ctx: Context):
        await ctx.send(embed=Embed(
            title="you threw a dice :game_die:",
            description=f"you rolled a :{['zero', 'one', 'two', 'three', 'four', 'five', 'six'][randint(1, 6)]}:",
            # todo expre -> var
            color=0xFF00AA
        ))

    @command("divergence", help="get your attractor field/divergence")
    async def divergence(self, ctx: Context):
        worldlines = {
            " ": "Omega",
            "0": "Alpha",
            "1": "Beta",
            "2": "Gamma",
            "3": "Delta"
        }
        divline = choice(list(worldlines.keys()))
        fstr = divline + "."
        for i in range(6):
            fstr += choice("0123456789")
        em = Embed(
            title="the divergence meter says",
            description=f"you are in the {worldlines[divline]} attractor field ({fstr.replace(' ', '-')})",
            color=0xFF00AA
        )
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Text())
