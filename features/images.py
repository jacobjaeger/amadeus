from discord.ext.commands import Cog, command, Context
from discord import Embed
from aiohttp import ClientSession
from .common import invalid_arg
from random import choice


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
        sub = ctx.bot.reddit.subreddit(subreddit)  # Fetch the requested subreddit
        if sub.over18 and not ctx.channel.is_nsfw():  # If the requested sub is NSFW but the current channel is not, the bot is supposed to stop working
            await ctx.send(embed=Embed(
                text="nsfw error",
                description="it seems like the sub you've request is nsfw while this channel is not, please try again in an nsfw channel",
                color=0xFF0000
            ))
            return
        em.set_image(url=choice([i for i in ctx.bot.reddit.subreddit(subreddit).hot(limit=50)]).url)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Images())
