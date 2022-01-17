# -*- coding: utf-8 -*-

from discord.ext import commands
import discord


class Fun(commands.Cog):
    """This is just random fun stuff"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx):
        """I repeat what you say"""
        await ctx.send(' '.join(ctx.message.content.split()[1:]))
        await ctx.message.delete()

    @commands.command(pass_context=True)
    async def dm(self, ctx: commands.Context, user: discord.Member = None, *, message):
        """DMs a user"""
        await user.send(message)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Fun(bot))
