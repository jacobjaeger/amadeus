from discord.ext.commands import Cog, command, Context, is_owner
from discord import Embed
from re import compile
from aiohttp import ClientSession
import hashlib
from typing import Optional
from .common import invalid_arg
import datetime


class Development(Cog):
    VER_CHECK = compile(r"^\d+(\.\d+(\.\d+)?)?$")

    def __init__(self):
        self.pyversion = "3"

    @command("pydoc", help="""look up the python documentation, optionally for a module or function. invoke without arguments to look up the base link for the python documentation online, with one argument (the module name) to look up a module or with two argument to look up a class/function/constant (arg 2) in a module (arg 1)""")
    async def pydoc(self, ctx: Context, *arg):
        if len(arg) == 0:
            await ctx.send(embed=Embed(
                title=f"python{self.pyversion} docs",
                description=f"[are located here](https://docs.python.org/{self.pyversion})",
                color=0xFF00AA
            ))
        elif len(arg) == 1:
            await ctx.send(embed=Embed(
                title=f"docs for python{self.pyversion} module {arg[0]}",
                description=f"[are located here](https://docs.python.org/{self.pyversion}/library/{arg[0]}.html)",
                color=0xFF00AA
            ))
        elif len(arg) == 2:
            await ctx.send(embed=Embed(
                title=f"docs for python{self.pyversion} function/class/constant {arg[0]}.{arg[1]}",
                description=f"[are located here](https://docs.python.org/{self.pyversion}/library/{arg[0]}.html#{arg[0]}.{arg[1]})", # noqa
                color=0xFF00AA
            ))
        else:
            await invalid_arg(ctx)

    @command("pyver", hidden=True)
    @is_owner()
    async def pyver(self, ctx: Context, *arg):
        if len(arg) == 0:
            await ctx.send(embed=Embed(
                title="the used doc version is",
                description=self.pyversion,
                color=0xFF00AA
            ))
        elif len(arg) == 1:
            if self.VER_CHECK.match(arg[0].strip()):
                ver = arg[0].strip()
                if len(ver.split(".")) == 3:
                    ver = ".".join(ver.split(".")[:-1])
                self.pyversion = ver
            else:
                await invalid_arg(ctx)
                return
            await ctx.send(embed=Embed(
                title="set new doc version",
                description="to " + self.pyversion,
                color=0x00FF00
            ))
        else:
            await invalid_arg(ctx)

    @command("cppdoc", help="""look up the c++ documentation online. invoke with zero arguments for the documentation base link. invoke with one argument (header name) to return a header documentation. invoke with two ore more arguments to look up a class/function/macro (2nd arg) or its members (3rd+ args) in a header (1st arg). the std namespace is optional and will be ignored for macros""")
    async def cppdoc(self, ctx: Context, *arg):
        if len(arg) == 0:
            await ctx.send(embed=Embed(
                title=f"c++ docs",
                description=f"[are located here](http://www.cplusplus.com/reference/)",
                color=0xFF00AA
            ))
        elif len(arg) == 1:
            await ctx.send(embed=Embed(
                title=f"docs for c++ header {arg[0]}",
                description=f"[are located here](http://www.cplusplus.com/reference/{arg[0]})",
                color=0xFF00AA
            ))
        else:
            fn = arg[1] if not arg[1].startswith("std::") else arg[1][5:]
            await ctx.send(embed=Embed(
                title=f"docs for {arg[1]}{'::' if len(arg[2:]) else ''}{'::'.join(arg[2:])} (header {arg[0]})",
                description=f"[are located here](http://www.cplusplus.com/reference/{arg[0]}/{fn}/{'/'.join(arg[2:])})",
                color=0xFF00AA
            ))

    @command("hash", help="""compute a sha hash of the type (optional, default = 256) of a text""")
    async def hash(self, ctx: Context, type: Optional[int] = 256, *, text):
        try:
            h = getattr(hashlib, "sha" + str(type))()
        except AttributeError:
            await ctx.send(embed=Embed(
                title="sha hash type not found",
                description=f"there seems to be no sha hash type sha{str(type)}",
                color=0xFF0000
            ))
            return
        h.update(bytes(text, encoding="utf-8"))
        e = Embed(
            title="original",
            description=text,
            color=0xFF00AA
        )
        e.set_author(name=f"sha{str(type)} hash", icon_url=ctx.bot.user.avatar_url)
        e.add_field(name="hash", value=h.hexdigest())
        await ctx.send(embed=e)

    @command("github", help="""look up a github user/repo""")
    async def github(self, ctx: Context, user, repo: Optional[str] = None):
        async with ClientSession() as s:
            if repo is None:
                async with s.get(f"https://api.github.com/users/{user}") as r:
                    if r.status == 404:
                        em = Embed(
                            title="user not found",
                            description=f"the specified user **{user}** does not exist",
                            color=0xFF0000
                        )
                    else:
                        data = await r.json()
                        em = Embed(
                            description=data["bio"],
                            color=0xFF00AA
                        )
                        em.add_field(
                            name="followers",
                            value=data["followers"]
                        )
                        em.add_field(
                            name="following",
                            value=data["following"]
                        )
                        em.add_field(
                            name="repos",
                            value=data["public_repos"]
                        )
                        created_at = datetime.datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                        em.add_field(
                            name="created at",
                            value=created_at
                        )
                        em.set_author(name=data["name"] if data["name"] is not None else data["login"], url=data["blog"] if "blog" in data else data["html_url"], icon_url=data["avatar_url"])
            else:
                async with s.get(f"https://api.github.com/repos/{user}/{repo}") as r:
                    if r.status == 404:
                        em = Embed(
                            title="repo not found",
                            description=f"the specified repo **{user}/{repo}** does not exist",
                            color=0xFF0000
                        )
                    else:
                        data = await r.json()
                        em = Embed(
                            description=data["description"] if data["description"] else "no description provided",
                            color=0xFF00AA
                        )
                        em.add_field(
                            name="license",
                            value=data['license']['name']
                        )
                        em.add_field(
                            name="language",
                            value=data["language"]
                        )
                        em.set_author(name=data["full_name"], url=data["homepage"] if data["homepage"] else data["html_url"], icon_url=data["owner"]["avatar_url"])
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Development())