from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pytz
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = os.environ['GOOGLE_DEV_APP_NAME']


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
    'calendar-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
        # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
    return credentials

def listOfEvents(event_dict):
    credentials = get_credentials()
    # print(credentials)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    new_event = service.events().insert(calendarId='primary', body=event_dict).execute()
    if not events:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))


def create_event(event_dict):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    start_time = event_dict["start"]["dateTime"]
    end_time = event_dict["end"]["dateTime"]
    eventsResult = service.events().list(
        calendarId='primary', timeMax=end_time, timeMin=start_time, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    event_list = eventsResult.get('items', [])
    if not event_list:
        new_event = service.events().insert(calendarId='primary', body=event_dict).execute()
        return [new_event["id"] , "added"]
    else:
        return "Busy"

def fourteen_day_schedule():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(
    calendarId='primary', timeMin=now,maxResults=100).execute()
    events = eventsResult.get('items', [])
    event_dict = {}
    for i in events:
        event_dict['summary'] = {
        "start_time" : i['start'],
        "end_time"   : i['end']
        }
    return event_dict

def cancel_event(event_id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    print("Cancelled")
    return "Cancelled"

# Can be used to debug this file individually
#if __name__ == "__main__":
    #create_event(user_suggest);
    #id = "dpntfuuh6ejnrktil3bb8ljmmg"
    #listOfEvents(user_suggest)
    #cancel_event(id)
