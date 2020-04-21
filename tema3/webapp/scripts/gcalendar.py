import os
import pickle
from datetime import datetime, timedelta
from pytz import timezone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

scopes = ['https://www.googleapis.com/auth/calendar.events']

credentials = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
credentials = os.path.join(credentials, 'client_secret_calendar.json').replace('\\', '/')
print(credentials)
credentials_pickle_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r'token.pickle')

flow = InstalledAppFlow.from_client_secrets_file(credentials, scopes=scopes)


def dump_credentials():
    pickle.dump(credentials, open(credentials_pickle_file_path, 'wb'))


def load_credentials():
    return pickle.load(open(credentials_pickle_file_path, 'rb'))


def add_event(advert):
    global credentials
    # print(advert)
    credentials = Credentials(load_credentials()['access_token'])

    calendar_service = build('calendar', 'v3', credentials=credentials)

    tz_location = 'Europe/Bucharest'
    tz = timezone(tz_location)
    start_time = advert.date
    end_time = start_time + timedelta(minutes=advert.duration)

    event = {
        'summary': advert.title,
        'location': advert.location,
        'description': advert.description,
        'start': {
            'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': tz_location,
        },
        'end': {
            'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': tz_location,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    res = calendar_service.events().insert(calendarId='primary', body=event).execute()
    return res
