from discord.ext.commands import Bot, CommandNotFound, MissingRequiredArgument, MissingPermissions, CommandInvokeError, \
    Context
from discord import Embed, Guild, Game, Forbidden
from os import listdir
from features.common import invalid_arg
from json import load
from argparse import FileType, ArgumentParser
from praw import Reddit
from datetime import datetime


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

    def log_error(self, msg):
        print(f"\033[31m{msg}\033[0m")

    def log(self, msg):
        print(f"\033[36m{msg}\033[0m")

    def is_premium(self, user):
        return False

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
        else:
            await context.send(embed=Embed(
                title=f"an internal error occured ({type(exception).__name__})",
                description=str(exception),
                color=0xFF0000
            ))
            self.log_error(type(exception).__name__ + ": " + str(exception))

    async def on_ready(self):
        self.log("bot is ready")
        self._owner_id = (
            await self.application_info()).owner.id  # this is set to be able to get the owner in a blocking manner through self.cmp_owner_id
        await self.change_presence(activity=Game(name=f"on {len(self.guilds)} servers"))

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


if __name__ == '__main__':
    argp = ArgumentParser("amadeus")
    argp.add_argument("--config", type=FileType("r"), default="config.json", dest="f")
    conf = argp.parse_args()
    with conf.f as f:
        config = load(f)
    useful = Useful(config, ("a!", "<@373252109753384960> "))
    useful.before_invoke(_check)
    for i in listdir("features"):
        if i != "__pycache__":
            useful.load_extension("features." + (i if not i.endswith(".py") else i[:-3]))
    useful.run(config["token"])
