import discord
from discord.ext import commands

# windows paths
path0 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\gsheetEvents.py'
path1 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\CDNEventsCleaner.py'
path2 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\CDNEvents.txt'
path3 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\blocked_words.txt'
TokenPath = 'C:\\Users\\stepan\\PycharmProjects\\CDN_token'
GuildPath = 'C:\\Users\\stepan\\PycharmProjects\\CDN_guild'
# linux paths
# path0='/home/pi/Desktop/scripts/CDN-Discord-Bot/gsheetEvents.py'
# path1='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEventsCleaner.py'
# path2='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'
# path3='/home/pi/Desktop/scripts/CDN-Discord-Bot/blocked_words.txt'
# TokenPath = '/home/pi/Desktop/scripts/CDN_token'
# GuildPath='/home/pi/Desktop/scripts/CDN_guild'

with open(GuildPath, 'r') as guil:
    global GUILD
    almostGuild = guil.read()
    GUILD = almostGuild
with open(TokenPath, 'r') as toke:
    global TOKEN
    almostToken = toke.read()
    TOKEN = almostToken
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="$", intents=intents)

with open(path3, 'r') as f:
    global badwords  # You want to be able to access this throughout the code
    words = f.read()
    badwords = words.split()


# new code stuff
@bot.command(name="ping")
async def ping(ctx: commands.Context):
    """See how long the bot takes to respond"""
    await ctx.send(f"Pong! {round(bot.latency) * 1000} ms")


@bot.command(name="status", pass_context=True)
@commands.has_role("CDN Bot creator")
async def status(ctx: commands.Context, *, new_status: str):
    """Sets the bot's status"""
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=new_status))


@status.error
async def no_admin(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("An unknown error has occurred")
    else:
        await ctx.send("You don't have the role required to do this", delete_after=15, tts=True)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Server commands"))
    #print(f'{bot.user} is connected to the following guild:\n {guild.name}(id: {guild.id})')
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(881386384202530837)
    bot1 = bot.get_user(881243826767945738)
    #members = '\n - '.join([member.name for member in guild.members])
    #print(f'Guild Members:\n - {members}')
    await channel.send(f'{bot1.mention} is online')


@bot.event
async def on_member_join(member):
    channell = bot.get_channel(881007767018700860)
    embed = discord.Embed(title=f"Welcome {member}",
                          description=f"Thanks for joining {member.guild.name}! \n Please go to {channell.mention} to "
                                      f"tell us your name and what your role is in CDN (There can be multiple roles)",
                          color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar_url)  # Set the embed's thumbnail to the member's avatar image!
    await channell.send(embed=embed)
    #    print(member, "just joined")
    await member.create_dm()
    await member.dm_channel.send(
        f"""Hi {member.name}, welcome to the CDN Discord server! Please go to the channel in the CDN Discord Server 
        that is called /#roles-name-change-requests and tell us what you do for CDN and what your name is""")


@bot.event
async def on_message_delete(message):
    """Logs message deletions"""
    author = message.author.display_name
    this_channel = message.channel
    #    print(author)
    content = message.content
    #    print(content)
    async for message in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
        deleter = message.user.name
    #    print(deleter)
    embed = discord.Embed(title=f"{author}'s message in {this_channel} was deleted by {deleter}", description="",
                          color=discord.Colour.red())
    embed.add_field(name=content, value="Deleted Message", inline=True)
    channel = bot.get_channel(881026004154482709)
    await channel.send(embed=embed)


@bot.event
async def on_message_edit(message_before, message_after):
    """Logs message edits"""
    if message_after.embeds != 0:
        return
    else:
        embed = discord.Embed(
            title=f"{message_before.author.display_name} edited a message in {message_before.channel}",
            description="", color=discord.Color.gold())
        embed.add_field(name=message_before.content, value="Before Edit", inline=True)
        embed.add_field(name=message_after.content, value="After edit", inline=True)
        channel = bot.get_channel(881026004154482709)
        await channel.send(embed=embed)


@bot.event
async def on_voice_state_update(member, before, after):
    """Adds/Removes Voice role when you join/leave a call"""
    role = discord.utils.get(member.guild.roles, name="Voice")
    if not before.channel and after.channel:
        await member.add_roles(role)
    elif before.channel and not after.channel:
        await member.remove_roles(role)


# more new code
@bot.command(name="welcome")
async def welcome(ctx: commands.Context, user: discord.User):
    """Sends the welcome message if someone needs instructions on what they have to do"""
    role_channel = bot.get_channel(881007767018700860)
    await ctx.send(
        f'Welcome, {user.display_name}, to CDN\'s Discord Server. Please go to {role_channel.mention} to tell us your '
        f'name and what your role(s) is/are in CDN. You can request certain roles with $giveme role')


@bot.command()
async def hello(ctx: commands.Context):
    """I say hello if you say hello"""
    if 'hello' in ctx.message.content.lower():
        await ctx.message.channel.send(f'Hello {ctx.message.author.mention}')


@bot.command(name="events")
async def events(ctx: commands.Context):
    """Shows events that club/team leaders have submitted to our spreadsheet"""
    exec(open(path0).read())
    #        print("getting google sheet")
    exec(open(path1).read())
    #        print("cleaning google sheet")
    cdn_events = open(path2, 'r')
    #        print("reading google sheet")
    await ctx.message.channel.send(cdn_events.read())
    await ctx.message.delete()


@bot.command("show")
async def show(ctx: commands.Context, user: discord.Member = None):
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


@bot.command("giveme")
@commands.has_role("CDN member")
async def giveme(ctx: commands.Context, *, role: discord.Role):
    """Gives a role to the person asking"""
    role_change = bot.get_channel(881007767018700860)
    message = ctx.message
    if role.name == "Voice":
        await ctx.send("You can't have this role", delete_after=15)
        await message.delete()
    elif message.channel == role_change:
        await message.author.add_roles(role)
        embed = discord.Embed(title=f"{message.author.display_name} requested {role.name}", description="",
                              color=discord.Colour.blue())
        embed.add_field(name=message.content, value="Role request", inline=True)
        log_chan = bot.get_channel(881026004154482709)
        await log_chan.send(embed=embed)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Roles can't be requested here. Please use {role_change.mention}",
                       delete_after=10)
        await message.delete()


@giveme.error
async def recruit(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("An unknown error has occurred")
    else:
        await ctx.send("Sorry, but recruits can't get roles", delete_after=15)


@bot.command(name="give", pass_context=True)
@commands.has_role("Producers")
async def give(ctx: commands.Context, user: discord.Member, role: discord.Role):
    """Gives a role to someone"""
    stephan = bot.get_user(675726066018680861)
    message = ctx.message
    if role == "Voice":
        await ctx.send("You can't give this role", delete_after=10)
        await message.delete()
    await user.add_roles(role)
    embed = discord.Embed(title=f"{message.author.display_name} requested {role.name} for {user.display_name}",
                          description="", color=discord.Colour.dark_blue())
    embed.add_field(name=message.content, value="Role requested", inline=True)
    log_chan = bot.get_channel(881026004154482709)
    await log_chan.send(embed=embed)
    await ctx.send(f"{role.name} given to {user.display_name}")
    await stephan.send(f"{role.name} given to {user.display_name} by {ctx.author.display_name}")


@give.error
async def no_producers(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("An unknown error has occurred")
    else:
        await ctx.send("You don't have the Producers role, so I can\'t give them this role", delete_after=15, tts=True)


@bot.command(name="createrole", pass_context=True)
@commands.has_role("Producers")
async def new_role(ctx: commands.Context, role_name):
    """Creates a role"""
    stephan = bot.get_user(675726066018680861)
    await ctx.guild.create_role(name=role_name)
    embed = discord.Embed(title=f"{ctx.author.display_name} created {role_name}",
                          description="", color=discord.Colour.orange())
    embed.add_field(name=ctx.message.content, value="Role Created", inline=True)
    log_chan = bot.get_channel(881026004154482709)
    await log_chan.send(embed=embed)
    await ctx.send(f"{role_name} was successfully created by {ctx.author.display_name}", delete_after=600)
    await stephan.send(f"{role_name} was created by {ctx.author.display_name}")


@new_role.error
async def no_producers(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("An unknown error has occurred")
    else:
        await ctx.send("You don't have the Producers role, so I can\'t create this role", delete_after=15)
        await ctx.send(f"Hey guys, {ctx.author.display_name} wanted to create a role!",
                       tts=True, delete_after=60)


@bot.command("clear")
@commands.has_role("Producers")
async def clear(ctx: commands.Context, *, num_delete):
    """Clears up to 25 messages, excluding your command"""
    num_clear = num_delete
    num_clear = int(num_clear)
    if num_clear > 25:
        num_clear = 25
    await ctx.channel.purge(limit=num_clear+1)
    await ctx.send(f"{ctx.message.author.nick} deleted the last {num_clear} messages", delete_after=30)


@clear.error
async def no_producers(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("An unknown error has occurred")
    else:
        await ctx.send("You don't have permission to bulk delete messages", delete_after=15)


#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    msg = message.content
#    mgs = []
#    for word in badwords:
#        if word in msg:
##            await message.delete()
#            await message.channel.send(f'{message.author.mention} That word is not allowed', delete_after=15)
#    event_channel = bot.get_channel(881550954527326228)
#    if "happy birthday" in message.content.lower():
#        await message.channel.send('Happy Birthday! 🎈🎉')
#    elif message.channel == event_channel:
#        yes = "⬆️"
#        no = "⬇️"
#        maybe = "↔"
#        await message.add_reaction(yes)
#        await message.add_reaction(no)
#        await message.add_reaction(maybe)


@bot.event
async def on_raw_reaction_add(reaction):
    gid = bot.get_guild(875158282422067230)
    role_message = 926424422175367218
    eid = reaction.emoji.id
    ename = reaction.emoji.name
    channel = bot.get_channel(reaction.channel_id)
    userid = gid.get_member(reaction.user_id)
    if reaction.message_id == role_message:
        if eid == 900172591141097602:
            await channel.send("Yes, this is in fact Stephan", tts=True, delete_after=60)
        if eid == 926404937049579520:
            role = discord.utils.get(gid.roles, name="I want to stream")
            await userid.add_roles(role)
        if ename == "🧑":
            role = discord.utils.get(gid.roles, name="Senior")
            await userid.add_roles(role)
        if eid == 926416491761528884:
            role = discord.utils.get(gid.roles, name="Junior")
            await userid.add_roles(role)
        if eid == 883773966290944042:
            role = discord.utils.get(gid.roles, name="Sophomore")
            await userid.add_roles(role)
        if eid == 883579348991492156:
            role = discord.utils.get(gid.roles, name="Freshman")
            await userid.add_roles(role)
        if ename == "⚓":
            role = discord.utils.get(gid.roles, name="Host")
            await userid.add_roles(role)
        if ename == "💻":
            role = discord.utils.get(gid.roles, name="Editor")
            await userid.add_roles(role)
        if ename == "✍️":
            role = discord.utils.get(gid.roles, name="Writer")
            await userid.add_roles(role)
        if ename == "📹" or ename == "📷":
            role = discord.utils.get(gid.roles, name="Cameras")
            await userid.add_roles(role)
        if ename == "🎧":
            role = discord.utils.get(gid.roles, name="Audio")
            await userid.add_roles(role)
        if ename == "😴":
            role = discord.utils.get(gid.roles, name="Afterhours")
            await userid.add_roles(role)
        if ename == "🏒":
            role = discord.utils.get(gid.roles, name="Hawkey Fan")
            await userid.add_roles(role)


@bot.event
async def on_raw_reaction_remove(reaction):
    gid = bot.get_guild(875158282422067230)
    role_message = 926424422175367218
    eid = reaction.emoji.id
    ename = reaction.emoji.name
    channel = bot.get_channel(reaction.channel_id)
    userid = gid.get_member(reaction.user_id)
    if reaction.message_id == role_message:
        if eid == 900172591141097602:
            await channel.send("How dare you remove Stephan", tts=True, delete_after=60)
        if eid == 926404937049579520:
            role = discord.utils.get(gid.roles, name="I want to stream")
            await userid.remove_roles(role)
        if ename == "🧑":
            role = discord.utils.get(gid.roles, name="Senior")
            await userid.remove_roles(role)
        if eid == 926416491761528884:
            role = discord.utils.get(gid.roles, name="Junior")
            await userid.remove_roles(role)
        if eid == 883773966290944042:
            role = discord.utils.get(gid.roles, name="Sophomore")
            await userid.remove_roles(role)
        if eid == 883579348991492156:
            role = discord.utils.get(gid.roles, name="Freshman")
            await userid.remove_roles(role)
        if ename == "⚓":
            role = discord.utils.get(gid.roles, name="Host")
            await userid.remove_roles(role)
        if ename == "💻":
            role = discord.utils.get(gid.roles, name="Editor")
            await userid.remove_roles(role)
        if ename == "✍️":
            role = discord.utils.get(gid.roles, name="Writer")
            await userid.remove_roles(role)
        if ename == "📹" or ename == "📷":
            role = discord.utils.get(gid.roles, name="Cameras")
            await userid.remove_roles(role)
        if ename == "🎧":
            role = discord.utils.get(gid.roles, name="Audio")
            await userid.remove_roles(role)
        if ename == "😴":
            role = discord.utils.get(gid.roles, name="Afterhours")
            await userid.remove_roles(role)
        if ename == "🏒":
            role = discord.utils.get(gid.roles, name="Hawkey Fan")
            await userid.remove_roles(role)


bot.run(TOKEN)
