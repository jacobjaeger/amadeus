from discord.ext.commands import Bot, CommandNotFound, MissingRequiredArgument, MissingPermissions, CommandInvokeError, \
    Context, BadArgument
from discord import Embed, Guild, Game, Forbidden
from os import listdir
from features.common import invalid_arg
from json import load
from argparse import FileType, ArgumentParser
from praw import Reddit
from datetime import datetime
from asyncio import get_event_loop, new_event_loop
import sqlite3
import aiosqlite


class Useful(Bot):
    version = (2, 23)

    def __init__(self, conf, *args, **kwargs):
        super(Useful, self).__init__(*args, **kwargs)
        self.conf = conf
        self.active_since = datetime.now()
        self.counter = 0
        self.reddit = Reddit(
            client_id=conf["reddit"]["client_id"],
            client_secret=conf["reddit"]["client_secret"],
            user_agent=conf["reddit"]["user_agent"]
        )
        self.sudo = False
        with sqlite3.connect(conf["dbf"]) as db:
            db.execute("create table if not exists servers (id, premium)")
            db.execute("create table if not exists users (id, premium, xp, badges)")
        self.started = False

    def log_error(self, msg):
        print(f"\033[31m{msg}\033[0m")

    def log(self, msg):
        print(f"\033[36m{msg}\033[0m")

    async def on_command_error(self, context, exception):
        if type(exception) == CommandNotFound:
            return
        elif type(exception) == MissingRequiredArgument:
            await invalid_arg(context)
        elif type(exception) == MissingPermissions:
            await context.send(embed=Embed(
                title="wait! that's illegal!",
                description=str(exception).lower(),
                color=0xFF0000
            ))
        elif type(exception) == CommandInvokeError:
            await self.on_command_error(context, exception.__cause__)
        elif type(exception) == Forbidden:
            try:
                await context.send(embed=Embed(
                    title=f"i can't do that",
                    description="i am missing permissions",
                    color=0xFF0000
                ))
            except Forbidden:
                pass
        elif type(exception) == BadArgument:
            await context.send(embed=Embed(
                title="invalid arguments",
                description=str(exception),
                color=0xFF0000
            ))
        else:
            await context.send(embed=Embed(
                title=f"an internal error occured ({type(exception).__name__})",
                description=str(exception),
                color=0xFF0000
            ))
            self.log_error(type(exception).__name__ + ": " + str(exception))

    async def on_ready(self):
        self._owner_id = (
            await self.application_info()).owner.id  # this is set to be able to get the owner in a blocking manner through self.cmp_owner_id
        await self.change_presence(activity=Game(name=f"on {len(self.guilds)} servers"))
        if not self.started:
            self.db = aiosqlite.connect(self.conf["dbf"])
            await self.db.__aenter__()
            self.started = True
        self.log("bot is ready")

    async def on_guild_join(self, server: Guild):
        self.log("joined server")
        await self.change_presence(activity=Game(name=f"on {len(self.guilds)} servers"))

    async def on_guild_remove(self, server: Guild):
        self.log("left server")
        await self.change_presence(activity=Game(name=f"on {len(self.guilds)} servers"))

    def cmp_owner_id(self, id):  # -> self.on_ready
        return id == self._owner_id

    async def is_premium(self, user):
        return False  # to be implemented


async def _check(ctx: Context):
    ctx.bot.counter += 1
    ctx.bot.log(
        f"[command called by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})] " + ctx.message.content)
    if ctx.command.__original_kwargs__.get("requires_db", False):
        async with ctx.bot.db.execute("select * from users where id = ?", (ctx.author.id,)) as c:
            res = await c.fetchone()
            if res is None:
                await c.execute("insert into users values (?, ?, ?, ?)", (ctx.author.id, False, 0, ""))
                await ctx.bot.db.commit()
                res = (ctx.author.id, False, 0, "")
            ctx.info = DBProxy(res)


async def _closing(ctx: Context):
    if not ctx.command.__original_kwargs__.get("requires_db", False):
        return
    await ctx.info.update(ctx.bot.db)
    del ctx.info


class DBProxy:
    def __init__(self, res):
        self._res = list(res)
        self._update = {}
        self._res[3] = res[3].split(":")
        self._before = self._res[3].copy()

    @property
    def xp(self):
        return self._res[2]

    @xp.setter
    def xp(self, value):
        if value != self.xp:
            self._update["xp"] = value

    @property
    def badges(self):
        return self._res[3] if "badges" not in self._update else self._update["badges"]

    @badges.setter
    def badges(self, other):
        if self.badges != other:
            self._update["badges"] = other

    @property
    def id(self):
        return self._res[0]

    @property
    def premium(self):
        return self._res[1]

    @premium.setter
    def premium(self, value):
        if value != self.premium:
            self._update["premium"] = value

    async def update(self, db):
        if len(self._update) == 0 and self._before == self._res[3]:
            return
        upd = self._update.copy()
        if "badges" in upd:
            if self._before == upd["badges"]:
                upd.pop("badges")
            else:
                upd["badges"] = ":".join(upd["badges"])
        else:
            if self._before != self._res[3]:
                upd["badges"] = ":".join(self._res[3])
        query = (
            f"update users set {', '.join([i + ' = ?' for i in upd.keys()])} where id = ?",
            list(upd.values()) + [self.id]
        )
        await db.execute(query[0], query[1])


if __name__ == '__main__':
    argp = ArgumentParser("amadeus")
    argp.add_argument("--config", type=FileType("r"), default="config.json", dest="f")
    argp.add_argument("--database", type=FileType("r"), default="amadeus.db", dest="db")
    conf = argp.parse_args()
    dbf = conf.db.name
    conf.db.close()
    with conf.f as f:
        config = load(f)
    config["dbf"] = dbf
    useful = Useful(config, ("a!", "<@373252109753384960> "))
    useful.before_invoke(_check)
    useful.after_invoke(_closing)
    for i in listdir("features"):
        if i != "__pycache__":
            useful.load_extension("features." + (i if not i.endswith(".py") else i[:-3]))
    try:
        useful.run(config["token"])
    finally:
        useful.db._loop = new_event_loop()
        useful.db._loop.run_until_complete(useful.db.__aexit__(None, None, None))
