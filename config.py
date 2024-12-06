import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv(dotenv_path='C:/Users/matth/PycharmProjects/iRacingDiscordBot/config.env')

comealBotToken = os.getenv('Discord_SECRET')
comealGuild = os.getenv('Comeal_GUILD')

iracing_user = os.getenv('iRacing_USER')
iracing_pass = os.getenv('iRacing_SECRET')

def get_previous_tuesday():
    today = datetime.now()
    # Weekday is an integer where Monday is 0 and Sunday is 6.
    weekday = today.weekday()
    # Calculate days since the last Tuesday.
    days_since_tuesday = (weekday - 1) % 7
    # Subtract those days to get to the previous Tuesday.
    last_tuesday = today - timedelta(days=days_since_tuesday)
    # Set time to the start of the day, if needed.
    last_tuesday_start = last_tuesday.replace(hour=0, minute=0, second=0, microsecond=0)
    return last_tuesday_start.strftime("%Y-%m-%dT%H:%MZ")