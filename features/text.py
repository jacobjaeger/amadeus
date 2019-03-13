from discord.ext.commands import Cog, command, Context
from discord import Embed, Member
import discord
from aiohttp import ClientSession
from .common import invalid_arg
from random import choice, randint
from typing import Optional, Union


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

    @command("info", help="show info about a member/channel")
    async def info(self, ctx: Context, item: Optional[Union[discord.Member, discord.TextChannel]] = None):
        em = Embed(color=0xFF00AA)
        em.set_footer(text=f"requested by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
        if type(item) == discord.Member:
            await self._info_user(em, ctx, item)
        elif type(item) == discord.TextChannel:
            await self._info_channel(em, ctx, item)
        elif type(item) == type(None):
            await self._info_user(em, ctx, ctx.author)
        await ctx.send(embed=em)

    async def _info_user(self, embed: Embed, ctx: Context, user: Member):
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.add_field(name="name", value=f"{user.name}#{user.discriminator}")
        embed.add_field(name="bot", value=str(user.bot).lower())
        embed.add_field(name="joined", value=user.joined_at)
        embed.add_field(name="created", value=user.created_at)
        embed.add_field(name="top role", value=user.top_role.name)
        embed.add_field(name="id", value=user.id)
        if type(user.activity) == discord.Spotify:
            name, val = "listening", f"{user.activity.artist} - {user.activity.title}"
        elif type(user.activity) == discord.Streaming:
            name, val = "streaming", f"[{user.activity.name}]({user.activity.url})"
        elif type(user.activity) == discord.Game:
            name, val = "playing", user.activity.name
        else:
            return
        embed.add_field(name=name, value=val)  # noqa

    async def _info_channel(self, embed: Embed, ctx: Context, channel: discord.TextChannel):
        embed.set_author(name=f"#{channel.name}", icon_url=channel.guild.icon_url)
        embed.add_field(name="id", value=channel.id)
        embed.add_field(name="nsfw", value=str(channel.is_nsfw()).lower())
        embed.add_field(name="created", value=channel.created_at)

    @command("jeopardy", help="shows a real jeopardy question/answer")
    async def jeopardy(self, ctx: Context):
        async with ClientSession() as s:
            async with s.get("http://jservice.io/api/random") as r:
                json = await r.json()
                json = json[0]
                em = Embed(
                    title=f"{json['question'].lower()} [{json['value']}$]",
                    description=f"||{json['answer']}||",
                    color=0xFF00AA
                )
                em.set_author(name="jeopardy!",
                              icon_url="http://img.brothersoft.com/icon/softimage/j/jeopardy_super_deluxe-359215-1271729985.jpeg")
                em.set_footer(text=json["category"]["title"])
                await ctx.send(embed=em)

    @command("number", help="shows a fact about the specified number")
    async def number(self, ctx: Context, n: int):
        async with ClientSession() as s:
            async with s.get(f"http://numbersapi.com/{n}") as r:
                em = Embed(
                    title=f"a fact about {n}",
                    description=await r.text(),
                    color=0xFF00AA
                )
                await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Text())
