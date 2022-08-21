# -*- coding: utf-8 -*-
import pytz
from discord.ext import commands, tasks
import discord
import datetime
import pytz

#lastId = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\variables\\last_audit_log_deletion'
lastId='/home/pi/Desktop/scripts/CDN-Discord-Bot/variables/last_audit_log_deletion'

global lastDeleteId

tz = datetime.timezone(datetime.timedelta(hours=-5))

lock_time = datetime.time(22, 0, tzinfo=tz)
unlock_time = datetime.time(6, 0, tzinfo=tz)


class AutomatedStuff(commands.Cog):
    """Stuff that the bot does on its own"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.server_lock.start()
        self.server_unlock.start()

    @tasks.loop(time=lock_time)
    async def server_lock(self):
        #print("lock")
        guild = self.bot.get_guild(875158282422067230)
        role = discord.utils.get(guild.roles, id=917447073182412830)
        #print(role)
        perms = guild.text_channels
        for channel in perms:
            if channel.category_id==875158282422067232:
                if channel.id == 978775667871215646:
                    print("line 38 ran")
                else:
                    #print(channel.name)
                    sleep = channel.overwrites_for(role)
                    sleep.send_messages = False
                    await channel.set_permissions(target=role, overwrite=sleep)

    @tasks.loop(time=unlock_time)
    async def server_unlock(self):
        #print("lock")
        guild = self.bot.get_guild(875158282422067230)
        role = discord.utils.get(guild.roles, id=917447073182412830)
        #print(role)
        perms = guild.text_channels
        for channel in perms:
            if channel.category_id==875158282422067232:
                if channel.id == 978775667871215646:
                    print("line 40-something ran")
                else:
                    #print(channel.name)
                    sleep = channel.overwrites_for(role)
                    sleep.send_messages = None
                    await channel.set_permissions(target=role, overwrite=sleep)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_join(self, member):
        channell = self.bot.get_channel(881007767018700860)
        embed = discord.Embed(title=f"Welcome {member}",
                              description=f"Thanks for joining {member.guild.name}! \n Please go to {channell.mention} to "
                                          f"tell us your name, grade, and what you do in CDN (if you know)",
                              color=discord.Color.green())
        embed.set_thumbnail(url=member.display_avatar)  # Set the embed's thumbnail to the member's avatar image!
        await channell.send(embed=embed)
        #    print(member, "just joined")
        await member.create_dm()
        await member.dm_channel.send(
            f"""Hi {member.name}, welcome to the CDN Discord server! Please go to the channel in the CDN Discord Server 
            that is called /#roles-name-change-requests and tell us who you are (name and grade) and what you do/plan on doing for CDN""")

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message_delete(self, message):
        """Logs message deletions"""
        if message.interaction:
            return
        if message.embeds>[]:
            return
        with open(lastId, 'r') as last_id:
            lastDeleteId = last_id.read()
        author = message.author.display_name
        this_channel = message.channel
        content = message.content
        async for message in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
            # print(message)
            this_id = str(message.id)
            if this_id == lastDeleteId:
                # print("deleted by author")
                deleter = author
            else:
                # print("deleted by mod")
                deleter = message.user.name
                lastDeleteId = this_id
                with open(lastId, 'w') as last_id:
                    last_id.write(str(lastDeleteId))
        embed = discord.Embed(title=f"{author}'s message in {this_channel} was deleted by {deleter}", description="",
                              color=discord.Colour.red())
        embed.add_field(name="Deleted message:", value=content, inline=True)
        channel = self.bot.get_channel(881026004154482709)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message_edit(self, message_before, message_after):
        """Logs message edits"""
        if message_after.embeds > []:
            return
        else:
            embed = discord.Embed(
                title=f"{message_before.author.display_name} edited a message in {message_before.channel}",
                description="", color=discord.Color.gold())
            embed.add_field(name="Before edit:", value=message_before.content, inline=True)
            embed.add_field(name="After edit:", value=message_after.content, inline=True)
            channel = self.bot.get_channel(881026004154482709)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if message.author.bot:
            return
        stephan = self.bot.get_user(675726066018680861)
        #print(message.channel.id)
        #print(message.content.lower())
        #if "lock" in message.content.lower():
        #    await self.server_unlock()
            #print("unlocked?")
        # below is for saying "happy birthday" if someone says it
        if "happy birthday" in message.content.lower():
            await message.channel.send('Happy Birthday! 🎈🎉')
        if message.author.id is not stephan.id:
            if "stephy" in message.content.lower() or "skruglov" in message.content.lower() or "krugie" in message.content.lower() or "screw" in message.content.lower() or "skrewglov" in message.content.lower() or "scruglov" in message.content.lower():
                await message.channel.send(f"It's stephan to you {message.author.mention}!", delete_after=10)
                await message.delete()
            print(message.author.id)
            print(stephan.id)
        # below is for adding reactions to messages in 'events'
        yes = "⬆️"
        no = "⬇️"
        maybe = "↔"
        if message.channel == self.bot.get_channel(881550954527326228):
            await message.add_reaction(yes)
            await message.add_reaction(no)
            await message.add_reaction(maybe)
        if isinstance(message.channel, discord.channel.DMChannel):
            if message.author.bot:
                return
            await message.channel.send("Please don\'t respond here, I can\'t do anything with the message", delete_after=10)
            await stephan.send(message.content, delete_after=3600)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, reaction):
        gid = self.bot.get_guild(875158282422067230)
        role_message = 926424422175367218
        bot_testing = self.bot.get_channel(949144781227954247)
        eid = reaction.emoji.id
        ename = reaction.emoji.name
        channel = self.bot.get_channel(reaction.channel_id)
        message_id = await channel.fetch_message(reaction.message_id)
        emoji = self.bot.get_emoji(eid)
        userid = gid.get_member(reaction.user_id)
        recruit = discord.utils.get(gid.roles, name="Recruit")
        #print(f"{eid}, {ename}")
        #print(f"reaction channel: {channel}, bot testing channel: {bot_testing}")
#        if channel==bot_testing:
#            await message_id.remove_reaction(emoji, userid)
#            print(f"removed reaction {eid}, {ename}")
#            await bot_testing.send(f"{eid}/{ename} reaction from {userid.display_name} was removed due to lack of roles")
        if reaction.message_id == role_message:
            if recruit in userid.roles:
                await channel.send(f"{userid.display_name}, you are a recruit and can't request roles yet", delete_after=10)
                print(f"{userid.display_name} tried to get role attached to {ename}")
                await message_id.remove_reaction(emoji, userid)
                return
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
                role = discord.utils.get(gid.roles, id=880250312823296070)
                await userid.add_roles(role)
            if ename == "💻":
                role = discord.utils.get(gid.roles, name="Editor")
                await userid.add_roles(role)
            if ename == "✍️":
                role = discord.utils.get(gid.roles, name="Reporter")
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
            if eid == 958196788689530941:
                role = discord.utils.get(gid.roles, name="Can edit from home")
                await userid.add_roles(role)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_remove(self, reaction):
        gid = self.bot.get_guild(875158282422067230)
        role_message = 926424422175367218
        eid = reaction.emoji.id
        ename = reaction.emoji.name
        channel = self.bot.get_channel(reaction.channel_id)
        userid = gid.get_member(reaction.user_id)
        role = discord.utils.get(gid.roles, name="Recruit")
        if reaction.message_id == role_message:
            if role in userid.roles:
                print(f"Reaction removed, {userid} is a recruit")
                return
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
                role = discord.utils.get(gid.roles, id=880250312823296070)
                await userid.remove_roles(role)
            if ename == "💻":
                role = discord.utils.get(gid.roles, name="Editor")
                await userid.remove_roles(role)
            if ename == "✍️":
                role = discord.utils.get(gid.roles, name="Reporter")
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
            if eid == 958196788689530941:
                role = discord.utils.get(gid.roles, name="Can edit from home")
                await userid.remove_roles(role)


async def setup(bot):
    await bot.add_cog(AutomatedStuff(bot))
