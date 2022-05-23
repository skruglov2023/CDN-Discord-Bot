# -*- coding: utf-8 -*-

from discord.ext import commands
import discord


class Fun(commands.Cog):
    """This is just random fun stuff"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def echo(self, ctx: commands.Context, *, message):
        """I repeat what you say"""
        if not ctx.interaction:
            await ctx.send(f'{message}')
            await ctx.message.delete()
        else:
            await ctx.send(f'{message}')

    @commands.hybrid_command(pass_context=True)
    async def dm(self, ctx: commands.Context, user: discord.Member = None, *, message):
        """DMs a user"""
        await user.send(message)
        await ctx.send(f"Message \"{message}\" sent to {user}", ephemeral=True)
        if not ctx.interaction:
            await ctx.message.delete()

    @commands.hybrid_command()
    async def joined(self, interaction: commands.Context, member: discord.Member = None):
        """Responds with date and time when a member joined."""
        # If no member is explicitly provided then we use the command user here
        member = member or interaction.author

        # The format_dt function formats the date time into a human readable representation in the official bot
        await interaction.send(f'{member} joined {discord.utils.format_dt(member.joined_at)}', ephemeral=True)


async def setup(bot):
    await bot.add_cog(Fun(bot))
