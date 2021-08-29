import discord
print("import complete")
path0='/home/pi/Desktop/scripts/CDN-Discord-Bot/gsheetEvents.py'
path1='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEventsCleaner.py'
path2='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'
TOKEN = "ODgxMjQzODI2NzY3OTQ1NzM4.YSqARQ.uzxZGj0HSzH1IyXzAgdiSjbdmVI"
print("paths set up")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$greetings'):
        # new method for sending messages
        await message.channel.send('Greetings and salutations!')
    elif message.content.startswith('$showevents'):
        exec(open(path0).read())
        exec(open(path1).read())
        CDNEvents=open(path2, 'r')
        await message.channel.send(CDNEvents.read())
    elif message.content.startswith('$'):
        await message.channel.send('Invalid Command')
#    print(message.content)
client.run(TOKEN)
