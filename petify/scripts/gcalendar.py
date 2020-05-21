import os
import pickle
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

scopes = ['https://www.googleapis.com/auth/calendar.events']

project_path = os.path.dirname(os.path.dirname(__file__))
credentials = os.path.join(project_path, 'config/client_secret_calendar.json')
credentials_pickle_file_path = os.path.join(project_path, 'token.pickle')

flow = InstalledAppFlow.from_client_secrets_file(credentials, scopes=scopes)


def dump_credentials():
    pickle.dump(credentials, open(credentials_pickle_file_path, 'wb'))


def load_credentials():
    return pickle.load(open(credentials_pickle_file_path, 'rb'))


def add_event_gcalendar(advert):
    global credentials
    credentials = Credentials(load_credentials()['access_token'])

    calendar_service = build('calendar', 'v3', credentials=credentials)

    tz_location = 'Europe/Bucharest'
    start_time = advert._start_date[:-5]
    end_time = advert._end_date[:-5]

    adv_title = advert._title
    adv_location = advert._location
    adv_description = advert._description
    event = {
        'summary': adv_title,
        'location': adv_location,
        'description': adv_description,
        'start': {
            'dateTime': start_time,
            'timeZone': tz_location,
        },
        'end': {
            'dateTime': end_time,
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
