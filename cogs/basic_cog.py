# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

#path = "C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\variables\\roles.txt"
#path0 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\gsheetEvents.py'
#path1 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\CDNEventsCleaner.py'
#path2 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\CDNEvents.txt'


path='/home/pi/Desktop/scripts/CDN-Discord-Bot/variables/roles.txt'
path0='/home/pi/Desktop/scripts/CDN-Discord-Bot/gsheetEvents.py'
path1='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEventsCleaner.py'
path2='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label = 'Proceed', style = discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Proceeding', ephemeral = True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label = 'Cancel', style = discord.ButtonStyle.green)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('No action taken', ephemeral = True)
        self.value = False
        self.stop()


class Basic(commands.Cog):
    """Anyone can use these"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    with open(path, 'r') as role_file:
        global av_roles  # You want to be able to access this throughout the code
        all_roles = role_file.read()
        av_roles = all_roles.split()

    @commands.hybrid_command(name = "ping", hidden = True)
    async def ping(self, ctx: commands.Context):
        """See how long the bot takes to respond"""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000, 1)} ms", ephemeral = True)

    @ping.error
    async def ping_error(self, ctx, error):
        await ctx.send(error)

    @commands.hybrid_command(name = "welcome")
    @commands.guild_only()
    async def welcome(self, ctx: commands.Context, user: discord.User):
        """Sends the welcome message if someone needs instructions on what they have to do"""
        role_channel = self.bot.get_channel(881007767018700860)
        await ctx.send(
            f'Welcome, {user.mention}, to CDN\'s Discord Server. Please go to {role_channel.mention} to tell us your '
            f'name and what your role(s) is/are in CDN. You can request certain roles with $giveme role',
            ephemeral = False)

    @welcome.error
    async def welcome_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("An unknown error has occurred")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Who do I send the instructions to again?", ephemeral = True)
        else:
            await ctx.send(error)

    @commands.hybrid_command()
    async def hello(self, ctx: commands.Context):
        """I say hello if you say hello"""
        if 'hello' in ctx.message.content.lower():
            await ctx.message.channel.send(f'Hello {ctx.message.author.mention}')

    @hello.error
    async def hello_error(self, ctx, error):
        await ctx.send("Either something is broken or you do not exist")

    @commands.hybrid_command(name = "events", aliases = ["showevents"])
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
        if not ctx.interaction:
            await ctx.message.delete()

    @events.error
    async def event_error(self, ctx, error):
        await ctx.send(error)

    @commands.hybrid_command("show")
    async def show(self, ctx: commands.Context, user: discord.Member = None):
        """Shows user's information"""
        message = ctx.message
        if user is None:
            user = ctx.author
        print(user)
        embed = discord.Embed(color = 0xdfa3ff, description = user.mention)
        embed.set_author(name = str(user), icon_url = user.display_avatar)
        embed.set_thumbnail(url = user.display_avatar)
        embed.add_field(name = "Joined", value = discord.utils.format_dt(user.joined_at))
        embed.add_field(name = "Registered", value = discord.utils.format_dt(user.created_at))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][2:])
            embed.add_field(name = "Roles:", value = role_string, inline = False)
        embed.set_footer(text = 'ID: ' + str(user.id))
        await ctx.send(embed = embed, ephemeral = True)
        if not ctx.interaction:
            await message.delete()

    @show.error
    async def show_error(self, ctx, error):
        # await ctx.send("Either something is broken or you do not exist")
        print(error)

    @commands.hybrid_command(name = "giveme", aliases = ["givemerole", "giverole"])
    @commands.guild_only()
    @commands.has_role("Fam")
    async def giveme(self, ctx: commands.Context, *, role: discord.Role):
        """Gives a role to the person asking"""
        role_change = self.bot.get_channel(881007767018700860)
        message = ctx.message
        if str(role.id) not in av_roles:
            # print("will not proceed to message")
            # print(f"Wanted {role}")
            # print(f"Roles available: {av_roles}")
            await ctx.send("You can't request this role", ephemeral = True)
            return
        elif message.channel == role_change:
            view = Confirm()
            await ctx.send('Are you sure you want this role?', view = view, ephemeral = True)
            await view.wait()
            # print(role.id)
            if view.value is None:
                return
            elif view.value:
                await message.author.add_roles(role)
                embed = discord.Embed(title = f"{message.author.display_name} requested {role.name}",
                                      color = discord.Colour.blue())
                # embed.add_field(name=role.name, value="Role request", inline=True)
                log_chan = self.bot.get_channel(978506865338114068)
                # print("role given")
                await log_chan.send(embed = embed)
                await ctx.send(embed = embed)
            else:
                await ctx.send("Role not given", ephemeral = True)
        else:
            await ctx.send(f"Roles can't be requested here. Please use {role_change.mention}", ephemeral = True)
        if not ctx.interaction:
            await message.delete()

    @giveme.error
    async def giveme_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("What role do you want?", delete_after = 15)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I can\'t give you that role due to discord hierarchy", delete_after = 15)
        elif isinstance(error, commands.MissingRole):
            await ctx.send("Recruits can\'t ask for roles", ephemeral = True)
        else:
            # await ctx.send("Some error has occurred, check log for more info")
            print(error)

    @commands.hybrid_command(name = "showroles", aliases = ["roles", "giveme roles", "givethem roles", "give roles"])
    @commands.guild_only()
    @commands.has_role("Fam")
    async def showroles(self, ctx):
        """Lists roles that can be given"""
        print(av_roles)
        role_names = [discord.utils.get(ctx.guild.roles, id = int(av_role)).mention for av_role in av_roles]
        roles_string = "\n".join(role_names)
        await ctx.send(f"Available Roles:\n{roles_string}", ephemeral = True)

    @commands.command(name = "vote", aliases = ["poll"])
    @commands.guild_only()
    @commands.has_role("Fam")
    async def poll(self, ctx: commands.Context, options = None):
        """Adds vote emojis to a message"""
        if options is not None:
            options = int(options)
        if options == 2 or options is None or not isinstance(options, int):
            await ctx.message.add_reaction('<:christianThumbsUp:887887292134473738>')
            await ctx.message.add_reaction('<:christianThumbsDown:887884542256500766>')
        else:
            numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            for number in numbers[:options]:
                await ctx.message.add_reaction(number)


async def setup(bot):
    await bot.add_cog(Basic(bot))
