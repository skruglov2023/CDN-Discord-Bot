import os

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
#path0='/home/pi/Desktop/scripts/CDN-Discord-Bot/gsheetEvents.py'
#path1='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEventsCleaner.py'
#path2='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'
#path3='/home/pi/Desktop/scripts/CDN-Discord-Bot/blocked_words.txt'
#TokenPath = '/home/pi/Desktop/scripts/CDN_token'
#GuildPath='/home/pi/Desktop/scripts/CDN_guild'

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


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Server commands"))
    # print(f'{bot.user} is connected to the following guild:\n {guild.name}(id: {guild.id})')
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(881386384202530837)
    bot1 = bot.get_user(881243826767945738)
    #members = '\n - '.join([user.display_name for user in guild.members])
    #print(f'Guild Members:\n - {members}')
    await channel.send(f'{bot1.mention} is online')
    cogs = ["cogs.admin_cog", "cogs.automated_cog", "cogs.basic_cog", "cogs.fun_cog"]
    for cog in cogs:
        bot.load_extension(cog)
    #for deleting dm messages
    #msgs=[]
    #for msg in msgs:
    #    await bot.http.delete_message(881403952875339817, msg)
    #    print(msg)


@bot.command(name="reload", pass_context=True, hidden=True)
@commands.has_role("CDN Bot creator")
async def reload_cog(ctx: commands.Context, reloadable):
    print(reloadable)
    """Reloads a cog after an update, instead of reloading the entire bot"""
    bot.reload_extension(f"cogs.{reloadable}")
    print(f"cog reloaded: {reloadable}")


@reload_cog.error
async def reload_cog_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don\'t have the required role to do this", delete_after=15)
    else:
        await ctx.send(error)

#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    msg = message.content
#    mgs = []
#    for word in badwords:
#        if word in msg:
#            await message.delete()
#            await message.channel.send(f'{message.author.mention} That word is not allowed', delete_after=15)

bot.run(TOKEN)
