import discord
import requests
from dateutil.tz import tzutc
from discord.ext import commands, tasks
import datetime
import dateutil.parser


class Calendar(commands.Cog):
    """This is for integrations with MeisterTask, Google Calendar, etc"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.auto_get_google_calendar_events.start()

    @tasks.loop(hours=24)
    async def auto_get_google_calendar_events(self):
        """Gets events from Google Calendar and creates Discord events"""
        events = requests.get(
            "https://www.googleapis.com/calendar/v3/calendars/c_8a7db21e614f5514cf46928d020ac30ca1462855700181e1fec5f626cc86c4b3@group.calendar.google.com/events?key=AIzaSyDLEgyeDYdZisERCW93f-O_K_5d2V4zFOA")
        content = events.json()
        guild = self.bot.get_guild(875158282422067230)
        current_events = '\n'.join([event.name for event in guild.scheduled_events])
        #print(current_events)
        for event in content["items"]:
            event_date = dateutil.parser.parse(event["start"]["dateTime"])
            event_end_date = dateutil.parser.parse(event["end"]["dateTime"])
            if event_date.date() < datetime.datetime.now().date():
                pass
            elif event["summary"] in current_events:
                pass
            elif "description" in event:
                await guild.create_scheduled_event(name=event["summary"], description=f"{event['description']}, {event['htmlLink']}", start_time = event_date, location = "CDN Studio", end_time = event_end_date)
                #print(f"Event Summary: {event['summary']}\nEvent Description: {event['description']}\nStart: {event['start']['dateTime']}\nCreator: {event['creator']['email']}\nCalendar Link: {event['htmlLink']}\n")
            else:
                #print(f"Event Summary: {event['summary']}\nStart: {event['start']['dateTime']}\nCreator: {event['creator']['email']}\nCalendar Link: {event['htmlLink']}\n")
                await guild.create_scheduled_event(name=event["summary"], description = event['htmlLink'], start_time = event_date, location = "CDN Studio", end_time = event_end_date)

    @commands.hybrid_command("get_calendar")
    async def get_google_calendar_events(self, ctx: commands.Context):
        """Gets events from Google Calendar and creates Discord events"""
        events = requests.get(
            "https://www.googleapis.com/calendar/v3/calendars/c_8a7db21e614f5514cf46928d020ac30ca1462855700181e1fec5f626cc86c4b3@group.calendar.google.com/events?key=AIzaSyDLEgyeDYdZisERCW93f-O_K_5d2V4zFOA")
        content = events.json()
        if content is None:
            return
        guild = ctx.guild
        current_events = '\n'.join([event.name for event in guild.scheduled_events])
        print(current_events)
        for event in content["items"]:
            event_date = dateutil.parser.parse(event["start"]["dateTime"])
            event_end_date = dateutil.parser.parse(event["end"]["dateTime"])
            if event_date.date() < datetime.datetime.now().date():
                pass
            elif event["summary"] in current_events:
                pass
            elif "description" in event:
                await ctx.guild.create_scheduled_event(name=event["summary"], description=f"{event['description']}, {event['htmlLink']}", start_time = event_date, location = "CDN Studio", end_time = event_end_date)
                #print(f"Event Summary: {event['summary']}\nEvent Description: {event['description']}\nStart: {event['start']['dateTime']}\nCreator: {event['creator']['email']}\nCalendar Link: {event['htmlLink']}\n")
            else:
                #print(f"Event Summary: {event['summary']}\nStart: {event['start']['dateTime']}\nCreator: {event['creator']['email']}\nCalendar Link: {event['htmlLink']}\n")
                await ctx.guild.create_scheduled_event(name=event["summary"], description = event['htmlLink'], start_time = event_date, location = "CDN Studio", end_time = event_end_date)
        await ctx.send("Events have been created", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Calendar(bot))
