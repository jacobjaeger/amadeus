from discord.ext.commands import Cog, command, Context, is_owner, Bot, Command
from discord import Embed
from typing import Optional


@command("help")
async def help(ctx: Context, command: Optional[str] = None):
    bot: Bot = ctx.bot
    if not command:
        emb: Embed = Embed(color=0xFF00AA)
        emb.set_author(name="all available commands | `a!<command name> <args...>`", icon_url=bot.user.avatar_url)
        for i in list(bot.cogs.items()):
            if not getattr(i[1], "hidden", False):
                emb.add_field(name=i[0].lower(), value=", ".join(['`' + i.name + '`' for i in i[1].get_commands() if not i.hidden]),
                              inline=False)
    else:
        if command not in bot.all_commands:
            emb: Embed = Embed(
                title="command not found",
                description=f"there seems to be no command with the name {command}",
                color=0xFF0000
            )
        else:
            cmd: Command = bot.all_commands[command]
            emb: Embed = Embed(
                title=f"{command}{(' (a.k.a ' + ', '.join(cmd.aliases) + ')') if cmd.aliases else ''}",
                description=cmd.help if cmd.help else 'no description provided',
                color=0xFF00AA
            )
            emb.set_footer(text=ctx.prefix + cmd.signature)
    await ctx.send(embed=emb)


def setup(bot):
    bot.remove_command("help")
    bot.add_command(help)
