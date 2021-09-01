import discord
from discord.ext import commands
#print("import complete")
path0='/home/pi/Desktop/scripts/CDN-Discord-Bot/gsheetEvents.py'
path1='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEventsCleaner.py'
path2='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'
path3='/home/pi/Desktop/scripts/CDN-Discord-Bot/blocked_words.txt'
TokenPath = '/home/pi/Desktop/scripts/token'
GuildPath='/home/pi/Desktop/scripts/guild'

with open(GuildPath, 'r') as guil:
    global GUILD
    almostGuild = guil.read()
    GUILD =  almostGuild
with open(TokenPath, 'r') as toke:
    global TOKEN
    almostToken = toke.read()
    TOKEN =  almostToken
bot = commands.Bot(command_prefix='!')

@bot.command(name='addrole')
async def online(ctx):
    member=ctx.message.author
    #role = discord.utils.get(bot.get_guild(ctx.guild.id).roles, id ="881392098304217108")
    await member.add_roles(guild_id='875158282422067230', user_id='675726066018680861', role.id='881392098304217108')
bot.run(TOKEN)
