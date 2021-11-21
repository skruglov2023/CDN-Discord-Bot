import discord
from discord.ext import commands
import asyncio
import time
#print("import complete")
path0='/home/pi/Desktop/scripts/CDN-Discord-Bot/gsheetEvents.py'
path1='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEventsCleaner.py'
path2='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'
path3='/home/pi/Desktop/scripts/CDN-Discord-Bot/blocked_words.txt'
TokenPath = '/home/pi/Desktop/scripts/CDN_token'
GuildPath='/home/pi/Desktop/scripts/CDN_guild'

with open(GuildPath, 'r') as guil:
    global GUILD
    almostGuild = guil.read()
    GUILD =  almostGuild
with open(TokenPath, 'r') as toke:
    global TOKEN
    almostToken = toke.read()
    TOKEN =  almostToken
intents = discord.Intents.default()
intents.members=True
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
    channel=client.get_channel(881386384202530837)
    bot=client.get_user(881243826767945738)
#    members = '\n - '.join([member.name for member in guild.members])
#    print(f'Guild Members:\n - {members}')
    await channel.send(f'{bot.mention} is online')

@client.event
async def on_member_join(member):
    channel = client.get_channel(875158282422067234)
    channell=client.get_channel(881007767018700860)
    embed=discord.Embed(title=f"Welcome {member}", description=f"Thanks for joining {member.guild.name}! \n Please go to {channell.mention} to tell us your name and what your role is in CDN (There can be multiple roles)", color=discord.Color.green()) # F-Strings!
    embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!
    await channel.send(embed=embed)
#    print(member, "just joined")
    await member.create_dm()
    await member.dm_channel.send(f"""Hi {member.name}, welcome to the CDN Discord server! Please go to the channel in the CDN Discord Server that is called /#roles-name-change-requests and tell us what you do for CDN and what your name is""")

@client.event
async def on_message_delete(message):
    author=message.author.nick
    this_channel=message.channel
#    print(author)
    content=message.content
#    print(content)
    async for message in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
        deleter=message.user.nick
#    print(deleter)
    embed=discord.Embed(title=f"{author}'s message in {this_channel} was deleted by {deleter}", description="", color=discord.Colour.red())
    embed.add_field(name=content, value="Deleted Message", inline=True)
    channel=client.get_channel(881026004154482709)
    await channel.send(embed=embed)

@client.event
async def on_message_edit(message_before, message_after):
    embed=discord.Embed(title=f"{message_before.author.display_name} edited a message in {message_before.channel}", description="", color=discord.Color.gold())
    embed.add_field(name= message_before.content ,value="Before Edit", inline=True)
    embed.add_field(name=message_after.content, value="After edit", inline=True)
    channel=client.get_channel(881026004154482709)
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
    id = client.get_guild(875158282422067230)
    event_channel=client.get_channel(881550954527326228)
    event_response_channel=client.get_channel(882667880028708874)
    channell=client.get_channel(881007767018700860)
    stephan=client.get_user(675726066018680861)
    role_change=client.get_channel(881007767018700860)
    producers=discord.utils.get(id.roles, id=880274405836599356)
#    print(producers)
    if message.author == client.user:
        return
    msg=message.content
#    print(msg)
    mgs = []
    for word in badwords:
        if word in msg:
            await message.delete()
            await message.channel.send(f'{message.author.mention} That word is not allowed', delete_after=15)
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif '$welcome' in message.content.lower():
        # new method for sending messages
        await message.channel.send(f'Welcome to CDN\'s Discord Server. Please go to {channell.mention} to tell us your name and what your role is in CDN (There can be multiple roles)')
    elif message.content.startswith('$showevents'):
        exec(open(path0).read())
#        print("getting google sheet")
        exec(open(path1).read())
#        print("cleaning google sheet")
        CDNEvents=open(path2, 'r')
#        print("reading google sheet")
        await message.channel.send(CDNEvents.read())
        await message.delete()
    elif message.content.startswith('$help'):
        if "roles" in message.content.lower():
            roles = '\n - '.join([role.name for role in id.roles])
#            print(f'Roles:\n - {roles}')
            help_string=roles
            embed=discord.Embed(title="Available CDN Discord Roles", description="", color=discord.Colour.from_rgb(234, 170, 0))
            embed.add_field(name='Use $giveme with any role above the CDN Events role \nKeep in mind that none of these roles give you anything special \n', value=help_string, inline=True)
            channel=message.channel
            await channel.send(embed=embed)
        else:
#            print("help")
            help_string=f"""
		$hello: I say hello to you
		$welcome: I tell you what to do if you recently joined and don\'t know what to do
		$showevents: I tell you what the next events are that CDN has been invited to
		$showme: Shows your name and profile picture
		$help: See this message again
		$giveme followed by a role that you want or need: You can\'t get mod, so don't bother trying to. If I can't give you a role, an admin will give it to you if necessary
		$showthem and user_id: Don't know why you need that, but it gives you the person's username and profile picture. You need developer mode enabled to get user_id
		$ with a non-command: I will respond with Invalid Command
		Autonomous program: When you post something in {event_channel.mention}, I will add 3 reactions, and will list the names of respondents in {event_response_channel.mention}
		All messages, when deleted or edited, will be recorded
		If you have any questions, please message {stephan.mention}"""
            embed=discord.Embed(title="CDN Bot Support", description="", color=discord.Colour.from_rgb(234, 170, 0))
            embed.add_field(name='Possible commands include:', value=help_string, inline=True)
            channel=message.channel
            await channel.send(embed=embed)
        await message.delete()
    elif message.content.startswith('$showme'):
        embed=discord.Embed(title=f"{message.author}", description="", color=discord.Color.green())
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)
        await message.delete()
    elif message.content.startswith('$showthem'):
        show=message.content
#        print(show)
        show=show[10:]
#        print(show)
        show_user= await client.fetch_user(show)
#        print(show_user)
        embed=discord.Embed(title=f"{show_user}", description="", color=discord.Color.blue())
        embed.set_thumbnail(url=show_user.avatar_url)
        await message.channel.send(embed=embed)
        await message.delete()
    elif 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')
    elif message.content.startswith("$giveme"):
        role_name=message.content
#        print(role_name)
        role_name=role_name[8:]
        if role_name=="Voice":
            await message.channel.send("You can't have this role", delete_after=10)
            await message.delete()
#        print(role_name)
        elif message.channel==role_change:
            role = discord.utils.get(id.roles, name=role_name)
#            print(role)
#            print(message.author)
            await message.author.add_roles(role)
            embed=discord.Embed(title=f"{message.author.display_name} requested {role_name}", description="", color=discord.Colour.blue())
            embed.add_field(name=message.content, value="Role request", inline=True)
            logChan=client.get_channel(881026004154482709)
            await logChan.send(embed=embed)
            if role in message.author.roles:
                await message.channel.send(f"{role_name} given to {message.author.display_name}", delete_after=60)
        else:
            await message.channel.send(f"Roles can't be requested here. Please use {role_change.mention}", delete_after=10)
            await message.delete()
    elif message.content.startswith("$give"):
        #print(message.content)
        if producers in message.author.roles:
            give_to=message.content
            #print(give_to)
            give_to=give_to.replace('!', '')
            #print(give_to)
            role_name=give_to[28:]
#            print(role_name)
            give_to=give_to[8:26]
#        print(f"Only the uid {give_to}")
#        print(message.author)
            giving=id.get_member(int(give_to))
#        print(stephan)
#            print(f"User's name {giving}")
            rolee = discord.utils.get(id.roles, name=role_name)
            await giving.add_roles(rolee)
            embed=discord.Embed(title=f"{message.author.display_name} requested {role_name} for {giving.display_name}", description="", color=discord.Colour.dark_blue())
            embed.add_field(name=message.content, value="Role requested", inline=True)
            logChan=client.get_channel(881026004154482709)
            await logChan.send(embed=embed)
            if rolee in giving.roles:
                await message.channel.send(f"{role_name} given to {giving.display_name}", delete_after=60)
        else:
            await message.channel.send("You don't have the Producers role, so I can\'t give them this role", delete_after=30)

    elif message.content.startswith("$clear"):
        if producers in message.author.roles:
           # print("can delete")
            num_clear=message.content
            num_clear=num_clear[7:]
            num_clear=int(num_clear)
            if num_clear>25:
                num_clear=25
            await message.channel.purge(limit=num_clear)
            #print("deleting messages")
            await message.channel.send(f"{message.author.nick} deleted the last {num_clear} messages", delete_after=30)
    elif (message.channel==event_channel):
        yes="⬆️"
        no="⬇️"
        maybe="↔"
        await message.add_reaction(yes)
        await message.add_reaction(no)
        await message.add_reaction(maybe)
    elif message.content.startswith("$"):
        await message.channel.send('Invalid Command: Try Again', delete_after=15)
        await message.delete()

@client.event
async def on_reaction_add(reaction, user):
    event_channel=client.get_channel(881550954527326228)
    event_response=client.get_channel(882667880028708874)
    if reaction.message.channel==event_channel:
        if user.bot == 1:       
            return None
        if str(reaction.emoji) == "⬆️":
#        entry.append(user.mention+" Responded with yes")
#            print(user.nick)
#            print(reaction.message.content)
            await event_response.send(f"{user.nick} can come to {reaction.message.content}")
        if str(reaction.emoji) == "⬇️":
            await event_response.send(f"{user.nick} cannot come to {reaction.message.content}")
        if str(reaction.emoji) == "↔": 
            await event_response.send(f"{user.nick} could potentially come to {reaction.message.content}")

client.run(TOKEN)
