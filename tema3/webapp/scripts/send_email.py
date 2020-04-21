import os
import base64
import pickle
from email.mime.text import MIMEText

from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
# cred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
#                          r'config/appengine_credentials.json')


def create_message(sender, to, subject, message_text):
    new_message = MIMEText(message_text)
    new_message['to'] = to
    new_message['from'] = sender
    new_message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(new_message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    try:
        new_message = (service.users().messages().send(userId=user_id, body=message).execute())
        return new_message
    except errors.HttpError as e:
        print(e)


def send_welcome_message(sender, to, name):
    creds = None
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r'config/token.pickle')):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r'config/token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r'config/client_secret_calendar.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r'config/token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    message = create_message(sender, to, f'Hello {name}', 'Welcome to our Cloud Computing Project!')
    send_message(service, 'me', message)
