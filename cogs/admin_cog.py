# -*- coding: utf-8 -*-

from discord.ext import commands
import discord


class Admin(commands.Cog):
    """Commands available only to Producers or other admins"""

    def __init__(self, bot):
        self.bot = bot
        
    def is_me():
        def predicate(ctx):
            return ctx.message.author.id == 675726066018680861 or ctx.message.author.id == 361537594112081951
        return commands.check(predicate) 

    @commands.command(name="status", pass_context=True, hidden=True)
    @is_me()
    async def status(self, ctx: commands.Context, *, new_status: str):
        """Sets the bot's status"""
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=new_status))

    @status.error
    async def not_creator(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot the status", delete_after=10)
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the role required to do this", delete_after=15, tts=True)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You\'re testing my patience now, stop trying to change the status on the bot", tts=True, delete_after=60)
        else:
            await ctx.send(error)

    @commands.command(name="give", pass_context=True, aliases=["givethemrole"])
    @commands.guild_only()
    @commands.has_role("Producers")
    async def give(self, ctx: commands.Context, user: discord.Member, role: discord.Role):
        """Gives a role to someone"""
        stephan = self.bot.get_user(675726066018680861)
        message = ctx.message
        if role == "Voice":
            await ctx.send("You can't give this role", delete_after=10)
            await message.delete()
        await user.add_roles(role)
        embed = discord.Embed(title=f"{message.author.display_name} requested {role.name} for {user.display_name}",
                              description="", color=discord.Colour.dark_blue())
        embed.add_field(name=message.content, value="Role requested", inline=True)
        log_chan = self.bot.get_channel(881026004154482709)
        await log_chan.send(embed=embed)
        await ctx.reply(f"{role.name} given to {user.display_name}", mention_author=False)
        await stephan.send(f"{role.name} given to {user.display_name} by {ctx.author.display_name}")

    @give.error
    async def no_producers(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the Producers role, so I can\'t give them this role", delete_after=15, tts=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Who was this role for again?", delete_after=15)
        else:
            await ctx.send("An unknown error has occurred")

    @commands.command(name="createrole", pass_context=True, aliases=["newrole", "createandgiverole"])
    @commands.guild_only()
    @commands.has_role("Producers")
    async def new_role(self, ctx: commands.Context, role_name):
        """Creates a role"""
        stephan = self.bot.get_user(675726066018680861)
        await ctx.guild.create_role(name=role_name)
        embed = discord.Embed(title=f"{ctx.author.display_name} created {role_name}",
                              description="", color=discord.Colour.orange())
        embed.add_field(name=ctx.message.content, value="Role Created", inline=True)
        log_chan = self.bot.get_channel(881026004154482709)
        await log_chan.send(embed=embed)
        await ctx.reply(f"{role_name} was successfully created by {ctx.author.display_name}", delete_after=600, mention_author=False)
        await stephan.send(f"{role_name} was created by {ctx.author.display_name}")

    @new_role.error
    async def no_producers(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the Producers role, so I can\'t create the role for you", delete_after=15, tts=True)
            await ctx.send(f"Hey guys, {ctx.author.display_name} wanted to create a role!",
                           tts=True, delete_after=60)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot the role\'s name", delete_after=15)
        else:
            await ctx.send(error)

    @commands.command("clear")
    @commands.guild_only()
    @commands.has_role("Producers")
    async def clear(self, ctx: commands.Context, *, num_delete):
        """Clears up to 25 messages, excluding your command"""
        num_clear = num_delete
        num_clear = int(num_clear)
        if num_clear > 25:
            num_clear = 25
        await ctx.channel.purge(limit=num_clear+1)
        await ctx.send(f"{ctx.message.author.nick} deleted the last {num_clear} messages", delete_after=30)

    @clear.error
    async def no_producers(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You don't have permission to bulk delete messages", delete_after=15)
        else:
            await ctx.send(error)


def setup(bot):
    bot.add_cog(Admin(bot))
