from discord.ext.commands import Cog, command, Context
from discord import Embed
from aiohttp import ClientSession
from .common import invalid_arg, get_nekos_life, NSFWError
from random import choice
from prawcore.exceptions import Redirect


class Images(Cog):
    @command("neko", help="""shows a sfw picture from [nekos.life](https://nekos.life)""")
    async def neko(self, ctx: Context):
        async with ClientSession() as c:
            async with c.get("https://nekos.life/api/v2/img/neko") as r:
                json = await r.json()
                em = Embed(color=0xFF00AA)
                em.set_author(name="here ya go")
                em.set_image(url=json["url"])
                await ctx.send(embed=em)

    @command("nekogif", help="""shows a neko gif from [nekos.life](https://nekos.life)""")
    async def nekogif(self, ctx: Context):
        async with ClientSession() as c:
            async with c.get("https://nekos.life/api/v2/img/ngif") as r:
                json = await r.json()
                em = Embed(color=0xFF00AA)
                em.set_author(name="here ya go")
                em.set_image(url=json["url"])
                await ctx.send(embed=em)

    @command("cat", help="shows a random cat picture")
    async def cat(self, ctx: Context):
        e = Embed(color=0xFF00AA)
        e.set_image(url="https://cataas.com/cat/gif")
        e.set_author(name="here ya go")
        await ctx.send(embed=e)

    @command("doggo", help="shows a random doggo")
    async def doggo(self, ctx: Context):
        async with ClientSession() as s:
            async with s.get("https://random.dog/woof.json") as r:
                json = await r.json()
                em = Embed(color=0xFF00AA)
                em.set_author(name="here ya go")
                em.set_image(url=json["url"])
                await ctx.send(embed=em)

    @command("shibe", help="shows a random shibe")
    async def shibe(self, ctx: Context):
        async with ClientSession() as s:
            async with s.get("http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true") as r:
                json = await r.json()
                em = Embed(color=0xFF00AA)
                em.set_author(name="here ya go")
                em.set_image(url=json[0])
                await ctx.send(embed=em)

    @command("bird", help="shows a random bird")
    async def bird(self, ctx: Context):
        async with ClientSession() as s:
            async with s.get("http://shibe.online/api/birds?count=1&urls=true&httpsUrls=true") as r:
                json = await r.json()
                em = Embed(color=0xFF00AA)
                em.set_author(name="here ya go")
                em.set_image(url=json[0])
                await ctx.send(embed=em)

    @command("fox", help="shows a random fox")
    async def fox(self, ctx: Context):
        async with ClientSession() as s:
            async with s.get("https://randomfox.ca/floof/") as r:
                json = await r.json()
                em = Embed(color=0xFF00AA)
                em.set_author(name="here ya go")
                em.set_image(url=json["image"])
                await ctx.send(embed=em)

    @command("deepfried", help="shows a random deepfried meme")
    async def deepfried(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_author(name="here ya go")
        em.set_image(url=choice([i for i in ctx.bot.reddit.subreddit("deepfriedmemes").hot(limit=50)]).url)
        await ctx.send(embed=em)

    @command("reddit", help="shows a picture from the specified subreddit")
    async def reddit(self, ctx: Context, subreddit):
        em = Embed(color=0xFF00AA)
        em.set_author(name="here ya go")
        try:
            sub = ctx.bot.reddit.subreddit(subreddit)  # Fetch the requested subreddit
        except Redirect:
            await ctx.send(embed=Embed(
                title="invalid subreddit",
                description="the specified subreddit does not exist",
                color=0xFF0000
            ))
            return
        if sub.over18 and not ctx.channel.is_nsfw():  # If the requested sub is NSFW but the current channel is not, the bot is supposed to stop working
            raise NSFWError("it seems like the sub you've request is nsfw while this channel is not, please try again in an nsfw channel")
        em.set_image(url=choice([i for i in ctx.bot.reddit.subreddit(subreddit).hot(limit=50)]).url)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Images())
