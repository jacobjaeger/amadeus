from discord import Embed
from discord.ext.commands import Context, Bot, check, MissingPermissions


async def invalid_arg(ctx):
    await ctx.send(embed=Embed(
        title="invalid arguments",
        description="usage: " + ctx.prefix + ctx.command.signature,
        color=0xFF0000
    ))


def tail(obj):
    print(obj)
    return obj


def perms_or_sudo(*args):
    def predicate(ctx: Context):
        if ctx.bot.sudo and ctx.bot.cmp_owner_id(ctx.author.id):
            return True
        has_perms = True
        perms = ctx.channel.permissions_for(ctx.author)
        if perms.administrator:
            return True
        for i in args:
            try:
                is_al = getattr(perms, i)
            except AttributeError:
                continue
            if not is_al:
                has_perms = False
        if not has_perms:
            raise MissingPermissions(args)
        return has_perms
    return check(predicate)



def setup(bot):
    pass
