# -*- coding: utf-8 -*-

from discord.ext import commands
import discord


class AutomatedStuff(commands.Cog):
    """Stuff that the bot does on its own"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
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
    async def on_message_delete(self, message):
        """Logs message deletions"""
        author = message.author.display_name
        this_channel = message.channel
        content = message.content
        async for message in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
            deleter = message.user.name
        embed = discord.Embed(title=f"{author}'s message in {this_channel} was deleted by {deleter}", description="",
                              color=discord.Colour.red())
        embed.add_field(name=content, value="Deleted Message", inline=True)
        channel = self.bot.get_channel(881026004154482709)
        await channel.send(embed=embed)

    @commands.Cog.listener()
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
    async def on_voice_state_update(self, member, before, after):
        """Adds/Removes Voice role when you join/leave a call"""
        role = discord.utils.get(member.guild.roles, name="Voice")
        if not before.channel and after.channel:
            await member.add_roles(role)
        elif before.channel and not after.channel:
            await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        gid = self.bot.get_guild(875158282422067230)
        role_message = 926424422175367218
        eid = reaction.emoji.id
        ename = reaction.emoji.name
        channel = self.bot.get_channel(reaction.channel_id)
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

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        gid = self.bot.get_guild(875158282422067230)
        role_message = 926424422175367218
        eid = reaction.emoji.id
        ename = reaction.emoji.name
        channel = self.bot.get_channel(reaction.channel_id)
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


def setup(bot):
    bot.add_cog(AutomatedStuff(bot))
