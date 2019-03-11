from discord.ext.commands import Cog, command, Context
from discord import Embed, Member
import discord
from aiohttp import ClientSession
from .common import invalid_arg
from random import choice, randint
from typing import Optional, Union


class Levels(Cog):
    @command("profile", help="shows a user profile")
    async def profile(self, ctx: Context, user: Optional[Member] = None):
        user = user if user else ctx.author
        em = Embed(color=0xFF00AA)
        em.set_author(name=user.display_name, icon_url=user.avatar_url)
        em.set_footer(text=f"requested by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
        badges = ""
        if await ctx.bot.is_owner(user):
            badges += f"[<:amadeus_owner:419177011324387329>](https://www.youtube.com/watch?v=DLzxrzFCyOs \"Amadeus Owner\")"
        if ctx.bot.is_premium(user):
            badges += f"[<:amadeus_premium:419176416823738389>](https://www.youtube.com/watch?v=DLzxrzFCyOs \"Amadeus Premium\")"
        if badges:
            em.add_field(name="badges", value=badges)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Levels())
