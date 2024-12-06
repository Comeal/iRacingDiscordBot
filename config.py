from iracingdataapi.client import irDataClient
from datetime import datetime, timedelta

comealBotToken = os.environ['DISORD_SECRET']

comealGuild = '823227580583772200'

iracing_user = "matthew130393@gmail.com"
iracing_pass = "iRacing_SECRET"

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
