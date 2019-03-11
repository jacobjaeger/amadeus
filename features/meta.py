from discord.ext.commands import Cog, command, Context
from discord import Embed
from datetime import datetime


class Meta(Cog):
    @command("support", help="get an invite to the support server")
    async def support(self, ctx: Context):
        await ctx.send(embed=Embed(
            title="if you need help",
            description=f"you can get it [here](https://discord.gg/{ctx.bot.conf['info']['invite']})",
            color=0xFF00AA
        ))

    @command("about", help="show info about the bot")
    async def about(self, ctx: Context):
        em = Embed(
            title="amadeus written by jcb1317",
        )
        em.set_footer(text="version " + ".".join([str(i) for i in ctx.bot.version]))
        await ctx.send(embed=em)

    @command("stats", help="shows bot stats")
    async def stats(self, ctx: Context):
        em = Embed(color=0xFF00AA)
        em.set_author(name="amadeus stats", icon_url=ctx.bot.user.avatar_url)
        em.add_field(name="uptime", value=datetime.now() - ctx.bot.active_since)
        em.add_field(name="started", value=ctx.bot.active_since)
        em.add_field(name="commands called", value=f"{str(ctx.bot.counter)} since last restart")
        em.add_field(name="servers", value=str(len(ctx.bot.guilds)))
        em.add_field(name="channels", value=str(len([i for i in ctx.bot.get_all_channels()])))
        em.add_field(name="members", value=str(len([i for i in ctx.bot.get_all_members()])))
        em.set_footer(text=f"requested by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Meta())
