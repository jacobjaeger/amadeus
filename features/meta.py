from discord.ext.commands import Cog, command, Context
from discord import Embed


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


def setup(bot):
    bot.add_cog(Meta())
