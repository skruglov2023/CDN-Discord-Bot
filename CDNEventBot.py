import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

import logging
#logging.basicConfig(level=logging.ERROR)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='lastBotRun.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# windows paths
#path0 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\gsheetEvents.py'
#path1 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\CDNEventsCleaner.py'
#path2 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\CDNEvents.txt'
#path3 = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\blocked_words.txt'
#TokenPath = 'C:\\Users\\stepan\\PycharmProjects\\CDN_token'
#GuildPath = 'C:\\Users\\stepan\\PycharmProjects\\CDN_guild'
# linux paths
path0='/home/pi/Desktop/scripts/CDN-Discord-Bot/gsheetEvents.py'
path1='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEventsCleaner.py'
path2='/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'
path3='/home/pi/Desktop/scripts/CDN-Discord-Bot/blocked_words.txt'
TokenPath = '/home/pi/Desktop/scripts/CDN_token'
GuildPath='/home/pi/Desktop/scripts/CDN_guild'

MY_GUILD = discord.Object(id=875158282422067230)
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
intents.message_content = True


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$', intents=intents, application_id=int(881243826767945738))
        self.initial_extensions = [
            'cogs.admin_cog',
            'cogs.basic_cog',
            'cogs.fun_cog',
            'cogs.automated_cog',
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)
            # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


bot = commands.Bot(command_prefix="$", intents=intents)
bot = MyBot()


with open(path3, 'r') as f:
    global badwords  # You want to be able to access this throughout the code
    words = f.read()
    badwords = words.split()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Server commands"))
    #print(f'{bot.user} is connected to the following guild:\n {guild.name}(id: {guild.id})')
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(949144781227954247)
    bot1 = bot.get_user(881243826767945738)
    #members = '\n - '.join([user.display_name for user in guild.members])
    #print(f'Guild Members:\n - {members}')
    await channel.send(f'{bot1.mention} is online')
    #for deleting dm messages
#    msgs=[918503766670585906]
#    for msg in msgs:
#        await bot.http.delete_message(881403952875339817, msg)
#        print(msg)


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Proceed', style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.green)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


@bot.hybrid_command()
async def ask(ctx: commands.Context):
    """Asks the user a question to confirm something."""
    # We create the view and assign it to a variable so we can wait for it later.
    view = Confirm()
    await ctx.send('Do you want to continue?', view=view, delete_after=120)
    # Wait for the View to stop listening for input...
    await view.wait()
    if view.value is None:
        print('Timed out...')
    elif view.value:
        print('Confirmed...')
    else:
        print('Cancelled...')


@bot.hybrid_command(name="reload", pass_context=True, hidden=True)
@commands.has_role("CDN Bot Creator")
async def reload_cog(ctx: commands.Context, reloadable):
#    print(reloadable)
    """Reloads a cog after an update, instead of reloading the entire bot"""
    await bot.reload_extension(f"cogs.{reloadable}")
    embed = discord.Embed(color=discord.colour.Color.blurple())
    embed.add_field(name="Cog reloaded", value=reloadable)
    await ctx.send(embed=embed)
    print(f"cog reloaded: {reloadable}")


@reload_cog.error
async def reload_cog_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don\'t have the required role to do this", delete_after=15)
    else:
        await ctx.send(error)


# This context menu command only works on members
@bot.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official bot
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}', ephemeral=True)


@bot.tree.context_menu(name="Let dictators/Franklin know")
async def report_message(interaction: discord.Interaction, message: discord.Message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to the CDN Dictators and Franklin.', ephemeral=True
    )

    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(881026004154482709)  # replace with your channel id

    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

    await log_channel.send(embed=embed, view=url_view)

bot.run(TOKEN)
