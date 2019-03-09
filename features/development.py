from discord.ext.commands import Cog, command, Context, is_owner
from discord import Embed
from re import compile
import hashlib
from typing import Optional
from .common import invalid_arg


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


def setup(bot):
    bot.add_cog(Development())