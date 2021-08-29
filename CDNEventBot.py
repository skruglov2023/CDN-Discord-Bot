import discord
#print("import complete")
path0='/home/pi/Desktop/scripts/CDN-Discord-Bot/gsheetEvents.py'
path1='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEventsCleaner.py'
path2='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'
path3='/home/pi/Desktop/scripts/CDN-Discord-Bot/blocked_words.txt'
TOKEN = "ODgxMjQzODI2NzY3OTQ1NzM4.YSqARQ.uzxZGj0HSzH1IyXzAgdiSjbdmVI"
#print("paths set up")
intents = discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)
#client = discord.Client()
with open(path3, 'r') as f:
    global badwords  # You want to be able to access this throughout the code
    words = f.read()
    badwords = words.split()
# Startup Information
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Server commands"))
   # print('Connected to bot: {}'.format(client.user.name))
   # print('Bot ID: {}'.format(client.user.id))    
    print('We have logged in as {0.user}'.format(client))
    channel=client.get_channel(881386384202530837)
    bot=client.get_user(881243826767945738)
    await channel.send(f'{bot.mention} is online')

@client.event
async def on_message_join(member):
    channel = client.get_channel(875158282422067234)
    channell=client.get_channel(881007767018700860)
    embed=discord.Embed(title=f"Welcome {member.mention}", description=f"Thanks for joining {member.guild.name}!") # F-Strings!
    embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!
    await member.channel.send(embed=embed)
    await member.channel.send(f'Welcome to CDN\'s Discord Server. Please go to {channell.mention} to tell us your name and what your role is in CDN (There can be multiple roles)')

#@client.event
#async def on_message(ctx, message):
    # don't respond to ourselves
#    if message.author == client.user:
#        return

#    messageContent = message.content
#    if len(messageContent) > 0:
#        if any(bad_word in messageContent for word in word_list):
#            if word in messageContent:
#                await message.delete()
#                await message.channel.send('That word is not permitted here. Please use a different one')
#@client.event
#async def clear(ctx, number):
#    mgs = [] #Empty list to put all the messages in the log
#    number = int(number) #Converting the amount of messages to delete to an integer
#    async for x in Client.logs_from(ctx.message.channel, limit = number):
#        mgs.append(x)
#    await Client.delete_messages(mgs)
@client.event
async def on_message_delete(message):
    #await on_message(message)
    embed=discord.Embed(title=f"{message.author} deleted a message", description="", color=discord.Colour.red())
    embed.add_field(name=message.content, value="Deleted Message", inline=True)
    channel=client.get_channel(881026004154482709)
    await channel.send(embed=embed)
@client.event
async def on_message_edit(message_before, message_after):
    embed=discord.Embed(title=f"{message_before.author} edited a message", description="", color=discord.Color.gold())
    embed.add_field(name= message_before.content ,value="Before Edit", inline=True)
    embed.add_field(name=message_after.content, value="After edit", inline=True)
    channel=client.get_channel(881026004154482709)
    await channel.send(embed=embed)

@client.event
async def on_message(message):
    channell=client.get_channel(881007767018700860)
    if message.author == client.user:
        return
    msg=message.content
    mgs = []
    for word in badwords:
        if word in msg:
            await message.delete()
            await message.channel.send(f'{message.author.mention} That word is not allowed')
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$welcome'):
        # new method for sending messages
        await message.channel.send(f'Welcome to CDN\'s Discord Server. Please go to {channell.mention} to tell us your name and what your role is in CDN (There can be multiple roles)')
    elif message.content.startswith('$showevents'):
        exec(open(path0).read())
        exec(open(path1).read())
        CDNEvents=open(path2, 'r')
        await message.channel.send(CDNEvents.read())
    elif message.content.startswith('$help'):
        help_string="Your possible commands are: \n $hello: I say hello to you \n $welcome: I tell you what to do if you recently joined and don\'t know what to do \n $showevents: I tell you what the next events are that CDN has been invited to \n $showme: Shows your name and profile picture \n $help: View this message again \n $ and any characters: I will respond with Invalid Command \n Any words that don\'t include $: I will ignore your text \n All messages, when deleted or edited, will be recorded by me"
        embed=discord.Embed(title="CDN Bot Support", description="", color=discord.Colour.from_rgb(234, 170, 0))
        embed.add_field(name=message.content, value=help_string, inline=True)
        channel=message.channel
        await channel.send(embed=embed)
    elif message.content.startswith('$showme'):
        embed=discord.Embed(title=f"{message.author}", description="", color=discord.Color.green()) # F-Strings!
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)
    elif message.content.startswith('$'):
        await message.channel.send('Invalid Command')
#    print(message.content)
client.run(TOKEN)
