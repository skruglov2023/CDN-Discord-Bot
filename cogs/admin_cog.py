# -*- coding: utf-8 -*-
import asyncio
import datetime
import typing

from discord.ext import commands
import discord

path="C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\variables\\roles.txt"
#path='/home/pi/Desktop/scripts/CDN-Discord-Bot/variables/roles.txt'


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value=None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Proceed', style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Proceeding', ephemeral=True)
        self.value=True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.green)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('No action taken', ephemeral=True)
        self.value=False
        self.stop()


class Admin(commands.Cog):
    """Commands available only to Producers or other admins"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot

    def is_me_or_hannah():  # alejandro trolling moment
        def predicate(ctx):
            return ctx.message.author.id==675726066018680861 or ctx.message.author.id==361537594112081951

        return commands.check(predicate)

    with open(path, 'r') as role_file:
        global av_roles  # You want to be able to access this throughout the code
        all_roles=role_file.read()
        av_roles=all_roles.split()

    @commands.hybrid_command(name="status", pass_context=True, hidden=True)
    @is_me_or_hannah()
    async def status(self, ctx: commands.Context, *, new_status: str):
        """Sets the bot's status"""
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=new_status))
        await ctx.send(f"Status changed to {new_status}", ephemeral=True)

    @status.error
    async def not_creator(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot the status", delete_after=10, ephemeral=True)
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the role required to do this", delete_after=15, tts=True)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You\'re testing my patience now, stop trying to change the status on the bot", tts=True,
                           delete_after=60)
            await ctx.send("why do you keep doing this to me", ephemeral=True)
        else:
            await ctx.send(error)

    @commands.hybrid_command(name="give", pass_context=True, aliases=["givethemrole", "givethem"])
    @commands.guild_only()
    @commands.has_any_role("Executive Producers", "Assistant Producers")
    async def give(self, ctx: commands.Context, user: discord.Member, role: discord.Role,
                   reason: typing.Optional[str] = None):
        """Gives a role to someone"""
        # stephan = self.bot.get_user(675726066018680861)
        message=ctx.message
        if str(role.id) not in av_roles:
            # print("will not proceed to message")
            # print(f"Wanted {role}")
            # print(f"Roles available: {av_roles}")
            await ctx.send("You can't give this role", ephemeral=True)
            return
        view=Confirm()
        await ctx.send('Are you sure you want to give them that role?', view=view, ephemeral=True, delete_after=30)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            await user.add_roles(role)
            embed=discord.Embed(title=f"{message.author.display_name} gave {role.name} to {user.display_name}",
                                color=discord.Colour.dark_blue())
            if reason is not None:
                embed.add_field(name=role.name, value=f"Role requested, reason being: {reason}", inline=True)
            log_chan=self.bot.get_channel(978506865338114068)
            await log_chan.send(embed=embed)
            # await ctx.reply(f"{role.name} given to {user.display_name}", mention_author=False)
            # await stephan.send(f"{role.name} given to {user.display_name} by {ctx.author.display_name}")
        else:
            await ctx.send("Role not given", ephemeral=True)

    @give.error
    async def no_producers(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the Producers role, so I can\'t give them this role", delete_after=15,
                           tts=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Who was this role for again?", delete_after=15)
        else:
            await ctx.send("An unknown error has occurred")

    @commands.hybrid_command(name="create_role", pass_context=True, aliases=["newrole", "createandgiverole"])
    @commands.guild_only()
    @commands.has_any_role("Executive Producers", "Assistant Producers")
    async def new_role(self, ctx: commands.Context, role_name, reason: typing.Optional[str] = None):
        """Creates a role"""
        # stephan = self.bot.get_user(675726066018680861)
        view=Confirm()
        await ctx.send('Are you sure you want to create this role?', view=view, ephemeral=True, delete_after=30)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            await ctx.guild.create_role(name=role_name)
            embed=discord.Embed(title=f"{ctx.author.display_name} created {role_name}",
                                description="", color=discord.Colour.orange())
            if reason is not None:
                embed.add_field(name=ctx.message.content, value=f"Role Created, reason being: {reason}", inline=True)
            log_chan=self.bot.get_channel(978506865338114068)
            await log_chan.send(embed=embed)
            await ctx.reply(f"{role_name} was successfully created by {ctx.author.display_name}", delete_after=600,
                            mention_author=False)
            # await stephan.send(f"{role_name} was created by {ctx.author.display_name}")
        else:
            await ctx.send("Role not created", ephemeral=True)

    @new_role.error
    async def no_producers(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the Producers role, so I can\'t create the role for you", delete_after=15,
                           tts=True)
            await ctx.send(f"Hey guys, {ctx.author.display_name} wanted to create a role!",
                           tts=True, delete_after=60)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot the role\'s name", delete_after=15)
        else:
            await ctx.send(error)

    @commands.hybrid_command("clear")
    @commands.guild_only()
    @commands.has_any_role("Executive Producers", "Assistant Producers")
    async def clear(self, ctx: commands.Context, *, num_delete):
        """Clears up to 99 messages, excluding your command"""
        num_clear=num_delete
        num_clear=int(num_clear)
        if num_clear>99:
            num_clear=99
        view=Confirm()
        await ctx.send(f'Are you sure you want to delete {num_clear} messages', view=view, ephemeral=True,
                       delete_after=30)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            await ctx.channel.purge(limit=num_clear+1)
            await ctx.send(f"{num_clear} messages have been deleted", ephemeral=True)
        else:
            return

    @clear.error
    async def no_producers(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You don't have permission to bulk delete messages", delete_after=15)
        else:
            await ctx.send(error)

    @commands.hybrid_command("sleep")
    @commands.guild_only()
    @commands.has_any_role("Executive Producers", "Assistant Producers")
    async def channel_lock(self, ctx: commands.Context, minutes: int = None):
        """Temporarily stops people from typing in the channel"""
        role=discord.utils.get(ctx.guild.roles, name="Fam")
        perms=ctx.channel.overwrites_for(role)
        perms.send_messages=False
        await ctx.channel.set_permissions(role, overwrite=perms)
        await ctx.send(f"Sleep! Or do some homework. You have {minutes} minutes to do so", delete_after=60)
        perms.send_messages=None
        if minutes is None:
            return
        await asyncio.sleep(minutes*60)
        await ctx.channel.set_permissions(role, overwrite=perms)
        await ctx.send("Channel unlocked, enjoy the rest of your day", delete_after=120)

    @commands.hybrid_command("unlock")
    @commands.guild_only()
    @commands.has_any_role("Executive Producers", "Assistant Producers")
    async def channel_unlock(self, ctx):
        """Reverts changes made through $sleep"""
        role=discord.utils.get(ctx.guild.roles, name="Fam")
        perms=ctx.channel.overwrites_for(role)
        perms.send_messages=True
        await ctx.channel.set_permissions(role, overwrite=perms)
        await ctx.send("Enjoy the rest of your day", delete_after=60)

    @commands.hybrid_command("timeout")
    @commands.guild_only()
    @commands.has_any_role("Executive Producers", "Assistant Producers")
    async def timeout(self, ctx: commands.Context, target: discord.Member, timeout: float, reason):
        """Times out user and logs it"""
        log_chan=self.bot.get_channel(978506865338114068)
        # print(timeout)
        # print(reason)
        timeout_embed=discord.Embed(title="Time out user", color=discord.Color.red())
        timeout_embed.add_field(name="User timed out", value=f"{target.display_name} | {target.mention}", inline=False)
        timeout_embed.add_field(name="Reason", value=reason, inline=False)
        timeout_embed.add_field(name="Time",
                                value=f"Starting at {datetime.datetime.strftime(datetime.datetime.now().astimezone(), '%Y-%m-%d %H:%M:%S')}, for {timeout} minutes",
                                inline=False)
        await target.timeout(datetime.datetime.now().astimezone()+datetime.timedelta(minutes=timeout), reason=reason)
        await log_chan.send(embed=timeout_embed)
        await ctx.send(f"User {target.mention} timed out for {timeout} minutes")

    # print(datetime.datetime.strftime('%Y-%m-%d %H:%M:%S'))
    #    print(datetime.datetime.strftime(datetime.datetime.now().astimezone(), '%Y-%m-%d %H:%M:%S'))

    #    if datetime.time.hour==22 and datetime.date.weekday() is not 4 or datetime.date.weekday() is not 5:
    #        server_lock()

    @commands.hybrid_command("users")
    @commands.guild_only()
    async def show_all_with_role(self, ctx: commands.Context, role: discord.Role):
        """Shows all users with role"""
        members='\n - '.join([user.mention for user in role.members])
        withrole=discord.Embed(title=f"Users with role {role.name}", color=discord.Color.brand_green())
        withrole.add_field(name=role.name, value=f"- {members}", inline=False)
        await ctx.send(embed=withrole, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Admin(bot))
