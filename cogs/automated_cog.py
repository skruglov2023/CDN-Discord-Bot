# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

#lastId = 'C:\\Users\\stepan\\PycharmProjects\\CDN-Discord-Bot\\variables\\last_audit_log_deletion'
lastId='/home/pi/Desktop/scripts/CDN-Discord-Bot/variables/last_audit_log_deletion'

global lastDeleteId


class AutomatedStuff(commands.Cog):
    """Stuff that the bot does on its own"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_join(self, member):
        channell = self.bot.get_channel(881007767018700860)
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

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message_delete(self, message):
        """Logs message deletions"""
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
        embed.add_field(name=content, value="Deleted Message", inline=True)
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
            embed.add_field(name=message_before.content, value="Before Edit", inline=True)
            embed.add_field(name=message_after.content, value="After edit", inline=True)
            channel = self.bot.get_channel(881026004154482709)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_voice_state_update(self, member, before, after):
        """Adds/Removes Voice role when you join/leave a call"""
        role = discord.utils.get(member.guild.roles, name="Voice")
        if not before.channel and after.channel:
            await member.add_roles(role)
        elif before.channel and not after.channel:
            await member.remove_roles(role)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if message.author.bot:
            return
        stephan = self.bot.get_user(675726066018680861)
        # below is for saying "happy birthday" if someone says it
        if "happy birthday" in message.content.lower():
            await message.channel.send('Happy Birthday! 🎈🎉')
        # below is for adding reactions to messages in 'events'
        yes = "⬆️"
        no = "⬇️"
        maybe = "↔"
        if message.channel == self.bot.get_channel(881550954527326228):
            await message.add_reaction(yes)
            await message.add_reaction(no)
            await message.add_reaction(maybe)

    #        if isinstance(message.channel, discord.channel.DMChannel):
    #            await message.channel.send("Please don\'t respond here, I can\'t do anything with the message", delete_after=10)
    #            await stephan.send(message.content, delete_after=60*60*12)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, reaction):
        gid = self.bot.get_guild(875158282422067230)
        role_message = 926424422175367218
        bot_testing = self.bot.get_channel(949144781227954247)
        eid = reaction.emoji.id
        ename = reaction.emoji.name
        channel = self.bot.get_channel(reaction.channel_id)
        userid = gid.get_member(reaction.user_id)
        role = discord.utils.get(gid.roles, name="Recruit")
        if reaction.message_id == role_message:
            if role in userid.roles:
                await channel.send(f"{userid.display_name}, you are a recruit and can't request roles yet", delete_after=60)
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
                await channel.send(f"{userid.display_name}, you are a recruit and can't request roles yet", delete_after=60)
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
            if eid == 958196788689530941:
                role = discord.utils.get(gid.roles, name="Can edit from home")
                await userid.remove_roles(role)


def setup(bot):
    bot.add_cog(AutomatedStuff(bot))
