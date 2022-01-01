import discord
from discord.ext import commands
import asyncio
import time

# print("import complete")
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
client = discord.Client(intents=intents)
with open(path3, 'r') as f:
    global badwords  # You want to be able to access this throughout the code
    words = f.read()
    badwords = words.split()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Server commands"))
    #    print(f'{client.user} is connected to the following guild:\n {guild.name}(id: {guild.id})')
    print(f'Logged in as {client.user}')
    channel = client.get_channel(881386384202530837)
    bot = client.get_user(881243826767945738)
    #    members = '\n - '.join([member.name for member in guild.members])
    #    print(f'Guild Members:\n - {members}')
    await channel.send(f'{bot.mention} is online')


@client.event
async def on_member_join(member):
    # channel = client.get_channel(875158282422067234)
    channell = client.get_channel(881007767018700860)
    embed = discord.Embed(title=f"Welcome {member}",
                          description=f"Thanks for joining {member.guild.name}! \n Please go to {channell.mention} to "
                                      f"tell us your name and what your role is in CDN (There can be multiple roles)",
                          color=discord.Color.green())  # F-Strings!
    embed.set_thumbnail(url=member.avatar_url)  # Set the embed's thumbnail to the member's avatar image!
    await channell.send(embed=embed)
    #    print(member, "just joined")
    await member.create_dm()
    await member.dm_channel.send(
        f"""Hi {member.name}, welcome to the CDN Discord server! Please go to the channel in the CDN Discord Server 
        that is called /#roles-name-change-requests and tell us what you do for CDN and what your name is""")


@client.event
async def on_message_delete(message):
    author = message.author.nick
    this_channel = message.channel
    #    print(author)
    content = message.content
    #    print(content)
    async for message in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
        deleter = message.user.nick
    #    print(deleter)
    embed = discord.Embed(title=f"{author}'s message in {this_channel} was deleted by {deleter}", description="",
                          color=discord.Colour.red())
    embed.add_field(name=content, value="Deleted Message", inline=True)
    channel = client.get_channel(881026004154482709)
    await channel.send(embed=embed)


@client.event
async def on_message_edit(message_before, message_after):
    embed = discord.Embed(title=f"{message_before.author.display_name} edited a message in {message_before.channel}",
                          description="", color=discord.Color.gold())
    embed.add_field(name=message_before.content, value="Before Edit", inline=True)
    embed.add_field(name=message_after.content, value="After edit", inline=True)
    channel = client.get_channel(881026004154482709)
    await channel.send(embed=embed)


@client.event
async def on_voice_state_update(member, before, after):
    role = discord.utils.get(member.guild.roles, name="Voice")
    if not before.channel and after.channel:
        await member.add_roles(role)
    elif before.channel and not after.channel:
        await member.remove_roles(role)


@client.event
async def on_message(message):
    gid = client.get_guild(875158282422067230)
    event_channel = client.get_channel(881550954527326228)
    event_response_channel = client.get_channel(882667880028708874)
    channell = client.get_channel(881007767018700860)
    stephan = client.get_user(675726066018680861)
    role_change = client.get_channel(881007767018700860)
    producers = discord.utils.get(gid.roles, id=880274405836599356)
    newbies = discord.utils.get(gid.roles, id=917447097849118760)
    #    print(producers)
    if message.author == client.user:
        return
    msg = message.content
    #    print(msg)
    mgs = []
    for word in badwords:
        if word in msg:
            await message.delete()
            await message.channel.send(f'{message.author.mention} That word is not allowed', delete_after=15)
    if 'hello' in message.content.lower():
        await message.channel.send(f'Hello {message.author.mention}')
    elif 'welcome' in message.content.lower():
        # new method for sending messages
        await message.channel.send(
            f'Welcome to CDN\'s Discord Server. Please go to {channell.mention} to tell us your name and what your '
            f'role(s) is/are in CDN. You can request certain roles with $giveme role')
    elif message.content.startswith('$showevents'):
        exec(open(path0).read())
        #        print("getting google sheet")
        exec(open(path1).read())
        #        print("cleaning google sheet")
        CDNEvents = open(path2, 'r')
        #        print("reading google sheet")
        await message.channel.send(CDNEvents.read())
        await message.delete()
    elif message.content.startswith('$help'):
        if "roles" in message.content.lower():
            roles = '\n - '.join([role.name for role in gid.roles])
            #            print(f'Roles:\n - {roles}')
            help_string = roles
            embed = discord.Embed(title="Available CDN Discord Roles", description="",
                                  color=discord.Colour.from_rgb(234, 170, 0))
            embed.add_field(
                name='Use $giveme with any role above the CDN Events role \nKeep in mind that none of these roles '
                     'give you anything special \n',
                value=help_string, inline=True)
            channel = message.channel
            await channel.send(embed=embed)
        else:
            #            print("help")
            help_string = f"""
		$welcome: I tell you what to do if you recently joined and don\'t know what to do
		$showevents: I tell you what the next events are that CDN has been invited to
		$showme: Shows your name and profile picture
		$help: See this message again
		$giveme followed by a role that you want or need: You can\'t get mod, so don't bother trying to. If I can't give you a role, an admin will give it to you if necessary
		$showthem and user_id: Don't know why you need that, but it gives you the person's username and profile picture. You need developer mode enabled to get user_id
		$ with a non-command: I will respond with Invalid Command
		Autonomous program: When you post something in {event_channel.mention}, I will add 3 reactions that you can respond to.
	    Message {stephan.mention} with any questions"""
            embed = discord.Embed(title="CDN Bot Support", description="", color=discord.Colour.from_rgb(234, 170, 0))
            embed.add_field(name='Possible commands include:', value=help_string, inline=True)
            channel = message.channel
            await channel.send(embed=embed)
        await message.delete()
    elif message.content.startswith('$showme'):
        embed = discord.Embed(title=f"{message.author}", description="", color=discord.Color.green())
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)
        await message.delete()
    elif message.content.startswith('$showthem'):
        show = message.content
        #        print(show)
        show = show[10:]
        #        print(show)
        show_user = await client.fetch_user(show)
        #        print(show_user)
        embed = discord.Embed(title=f"{show_user}", description="", color=discord.Color.blue())
        embed.set_thumbnail(url=show_user.avatar_url)
        await message.channel.send(embed=embed)
        await message.delete()
    elif 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')
    elif message.content.startswith("$giveme"):
        role_name = message.content
        #        print(role_name)
        role_name = role_name[8:]
        if role_name == "Voice":
            await message.channel.send("You can't have this role", delete_after=15)
            await message.delete()
        #        print(role_name)
        elif newbies in message.author.roles:
            await message.channel.send(f"If you need a role, please ask {stephan.name} or another {producers.name}",
                                       delete_after=30)
            await message.delete()
        elif message.channel == role_change:
            role = discord.utils.get(gid.roles, name=role_name)
            #            print(role)
            #            print(message.author)
            await message.author.add_roles(role)
            embed = discord.Embed(title=f"{message.author.display_name} requested {role_name}", description="",
                                  color=discord.Colour.blue())
            embed.add_field(name=message.content, value="Role request", inline=True)
            logChan = client.get_channel(881026004154482709)
            await logChan.send(embed=embed)
            if role in message.author.roles:
                await message.channel.send(f"{role_name} given to {message.author.display_name}", delete_after=60)
        else:
            await message.channel.send(f"Roles can't be requested here. Please use {role_change.mention}",
                                       delete_after=10)
            await message.delete()
    elif message.content.startswith("$give"):
        give_to = message.content
        # print(give_to)
        give_to = give_to.replace('!', '')
        # print(give_to)
        role_name = give_to[28:]
        #       print(role_name)
        give_to = give_to[8:26]
        if role_name == "Voice":
            await message.channel.send("You can't give this role", delete_after=10)
            await message.delete()
        # print(message.content)
        elif producers in message.author.roles:
            giving = gid.get_member(int(give_to))
            #            print(f"User's name {giving}")
            rolee = discord.utils.get(gid.roles, name=role_name)
            await giving.add_roles(rolee)
            embed = discord.Embed(
                title=f"{message.author.display_name} requested {role_name} for {giving.display_name}", description="",
                color=discord.Colour.dark_blue())
            embed.add_field(name=message.content, value="Role requested", inline=True)
            logChan = client.get_channel(881026004154482709)
            await logChan.send(embed=embed)
            if rolee in giving.roles:
                await message.channel.send(f"{role_name} given to {giving.display_name}", delete_after=60)
        else:
            await message.channel.send("You don't have the Producers role, so I can\'t give them this role",
                                       delete_after=30)
            await message.channel.send(f"Hey guys, {message.author.display_name} wanted to give someone a role!",
                                       tts=True, delete_after=60)
    # new text here
    elif message.content.startswith("$newrole"):
        role_name = message.content
        give_to = role_name.replace('!', '')
        role_name = give_to[35:]
        #        print(role_name)
        give_to = give_to[15:33]
        #        print(give_to)
        if producers in message.author.roles:
            await gid.create_role(name=role_name)
            giving = gid.get_member(int(give_to))
            #            print(f"User's name {giving}")
            rolee = discord.utils.get(gid.roles, name=role_name)
            await giving.add_roles(rolee)
            embed = discord.Embed(title=f"{message.author.display_name} created {role_name} for {giving.display_name}",
                                  description="", color=discord.Colour.orange())
            embed.add_field(name=message.content, value="Role Created", inline=True)
            logChan = client.get_channel(881026004154482709)
            await logChan.send(embed=embed)
            #            if role_name in giving.roles:
            await message.channel.send(
                f"{role_name} was successfully created by {message.author.display_name} and given to {giving.display_name}",
                delete_after=600)
            await stephan.create_dm()
            await stephan.dm_channel.send(
                f"{role_name} was created by {message.author.display_name} for {giving.display_name}")
        else:
            await message.channel.send("You don't have the Producers role, so you can't be creating roles",
                                       delete_after=30)
            await message.channel.send(
                f"Hey guys, {message.author.display_name} wanted to create and give someone a role!", tts=True,
                delete_after=60)

    elif message.content.startswith("$clear"):
        if producers in message.author.roles:
            # print("can delete")
            num_clear = message.content
            num_clear = num_clear[7:]
            num_clear = int(num_clear)
            if num_clear > 25:
                num_clear = 25
            await message.channel.purge(limit=num_clear)
            # print("deleting messages")
            await message.channel.send(f"{message.author.nick} deleted the last {num_clear} messages", delete_after=30)
        else:
            await message.channel.send("You don't have permission to bulk delete messages", delete_after=15)
    elif message.channel == event_channel:
        yes = "⬆️"
        no = "⬇️"
        maybe = "↔"
        await message.add_reaction(yes)
        await message.add_reaction(no)
        await message.add_reaction(maybe)
    elif message.content.startswith("$"):
        await message.channel.send('Invalid Command: Try Again', delete_after=10)
        await message.delete()


@client.event
async def on_raw_reaction_add(reaction):
    gid = client.get_guild(875158282422067230)
    role_message = 926424422175367218
    eid = reaction.emoji.id
    ename = reaction.emoji.name
    channel = client.get_channel(reaction.channel_id)
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


@client.event
async def on_raw_reaction_remove(reaction):
    gid = client.get_guild(875158282422067230)
    role_message = 926424422175367218
    eid = reaction.emoji.id
    ename = reaction.emoji.name
    channel = client.get_channel(reaction.channel_id)
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


client.run(TOKEN)
