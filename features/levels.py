from discord.ext.commands import Cog, command, Context
from discord import Embed, Member
import discord
from aiohttp import ClientSession
from random import choice, randint
from typing import Optional, Union


class Levels(Cog):
    PROG = {
        "left": [482263833524699156, 482263833155731465],
        "center": [482263832744689665, 482263832757272577],
        "right": [482263832945754113, 482263833000542208]
    }

    @classmethod
    def level_from_xp(cls, xp):
        level = 0
        while True:
            if xp >= cls.xp_for_increase(level):
                xp -= cls.xp_for_increase(level)
                level += 1
            else:
                break
        return level

    @classmethod
    def progress_from_xp(cls, xp):
        lower_level = cls.level_from_xp(xp)
        upper_level = cls.xp_from_level(lower_level + 1)
        lower_level = cls.xp_from_level(lower_level)
        span = upper_level - lower_level
        prog = xp - lower_level
        return prog / span

    @classmethod
    def xp_from_level(cls, level):
        return sum([cls.xp_for_increase(i) for i in range(level)])

    @staticmethod
    def xp_for_increase(level):
        return 125 + sum([i * 5 for i in range(level + 1)])

    def make_pp(self, prog, step, stop):
        if prog >= step / stop:
            active = True
        else:
            active = False
        if step == 1:
            spec = "left"
        elif step == stop:
            spec = "right"
        else:
            spec = "center"
        return f"<:prog{spec}{'in' if not active else ''}active:{self.PROG[spec][int(not active)]}>"

    @command("profile", help="shows a user profile", requires_db=True)
    async def profile(self, ctx: Context, user: Optional[Member] = None):
        # user = user if user else ctx.author
        if user:
            info = await ctx.info.make(ctx.bot.db, user.id)
        else:
            info = ctx.info
            user = ctx.author
        em = Embed(color=0xFF00AA)
        em.set_author(name=user.display_name, icon_url=user.avatar_url)
        em.set_footer(text=f"requested by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
        prog_width = 8 if ctx.author.is_on_mobile() else 12
        prog = self.progress_from_xp(info.xp)
        pb = "".join([self.make_pp(prog, i, prog_width) for i in range(1, prog_width + 1)])
        lvl = self.level_from_xp(info.xp)
        a, b = info.xp - self.xp_from_level(lvl), self.xp_for_increase(lvl)
        em.add_field(name=f"progress (level {lvl} - {a}/{b} xp)", value=f"**{lvl}** {pb} **{lvl + 1}**", inline=False)
        badges = ""
        if await ctx.bot.is_owner(user):
            badges += f"[<:amadeus_owner:419177011324387329>](https://www.youtube.com/watch?v=DLzxrzFCyOs \"Amadeus Owner\")"
        if info.premium:
            badges += f"[<:amadeus_premium:419176416823738389>](https://www.youtube.com/watch?v=DLzxrzFCyOs \"Amadeus Premium\")"
        em.add_field(name="badges", value=badges if badges else "none")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Levels())
