import dateutil.parser

from O365 import Account
from models.Advert import Advert


def add_event(account: Account, advert: Advert):
    schedule = account.schedule()

    calendar = schedule.get_default_calendar()
    new_event = calendar.new_event()
    new_event.subject = advert.description
    new_event.location = advert.location

    new_event.start = dateutil.parser.isoparse(advert.start_date)
    new_event.end = dateutil.parser.isoparse(advert.end_date)

    new_event.remind_before_minutes = 45

    new_event.save()
