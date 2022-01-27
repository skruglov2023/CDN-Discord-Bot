# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
path0 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\gsheetEvents.py'
path1 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\CDNEventsCleaner.py'
path2 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\CDNEvents.txt'
#path0='/home/pi/Desktop/scripts/CDN-Discord-Bot/gsheetEvents.py'
#path1='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEventsCleaner.py'
#path2='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'


class Basic(commands.Cog):
    """Anyone can use these"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", hidden=True)
    async def ping(self, ctx: commands.Context):
        """See how long the bot takes to respond"""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000, 1)} ms")

    @ping.error
    async def ping_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(name="welcome")
    @commands.guild_only()
    async def welcome(self, ctx: commands.Context, user: discord.User):
        """Sends the welcome message if someone needs instructions on what they have to do"""
        role_channel = self.bot.get_channel(881007767018700860)
        await ctx.send(
            f'Welcome, {user.display_name}, to CDN\'s Discord Server. Please go to {role_channel.mention} to tell us your '
            f'name and what your role(s) is/are in CDN. You can request certain roles with $giveme role')

    @welcome.error
    async def welcome_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Who do I send the instructions to again?", delete_after=10)
        else:
            await ctx.send(error)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        """I say hello if you say hello"""
        if 'hello' in ctx.message.content.lower():
            await ctx.message.channel.send(f'Hello {ctx.message.author.mention}')

    @hello.error
    async def hello_error(self, ctx, error):
        await ctx.send("Either something is broken or you do not exist")

    @commands.command(name="events")
    @commands.guild_only()
    async def events(self, ctx: commands.Context):
        """Shows events that club/team leaders have submitted to our spreadsheet"""
        exec(open(path0).read())
        #        print("getting google sheet")
        exec(open(path1).read())
        #        print("cleaning google sheet")
        cdn_events = open(path2, 'r')
        #        print("reading google sheet")
        await ctx.message.channel.send(cdn_events.read())
        await ctx.message.delete()

    @events.error
    async def event_error(self, ctx, error):
        await ctx.send(error)

    @commands.command("show")
    async def show(self, ctx: commands.Context, user: discord.Member = None):
        """Shows user's information"""
        message = ctx.message
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][2:])
            embed.add_field(name="Roles:", value=role_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        await message.channel.send(embed=embed)
        await message.delete()

    @show.error
    async def show_error(self, ctx, error):
        await ctx.send("Either something is broken or you do not exist")

    @commands.command("giveme")
    @commands.guild_only()
    @commands.has_role("CDN member")
    async def giveme(self, ctx: commands.Context, *, role: discord.Role):
        """Gives a role to the person asking"""
        role_change = self.bot.get_channel(881007767018700860)
        message = ctx.message
        if role.name == "Voice":
            await ctx.send("You can't have this role", delete_after=15)
            await message.delete()
        elif message.channel == role_change:
            await message.author.add_roles(role)
            embed = discord.Embed(title=f"{message.author.display_name} requested {role.name}", description="",
                                  color=discord.Colour.blue())
            embed.add_field(name=message.content, value="Role request", inline=True)
            log_chan = self.bot.get_channel(881026004154482709)
            await log_chan.send(embed=embed)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Roles can't be requested here. Please use {role_change.mention}",
                           delete_after=10)
            await message.delete()

    @giveme.error
    async def giveme_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("What role do you want?", delete_after=15)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I can\'t give you that role due to discord hierarchy", delete_after=15)
        elif isinstance(error, commands.MissingRole):
            await ctx.send("Recruits can\'t ask for roles", delete_after=15)
        else:
            await ctx.send(error)


def setup(bot):
    bot.add_cog(Basic(bot))
