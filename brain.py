# This is a public client access token, when there's a server,
# this must be changed to a server-side token
from wit import Wit
import inspect
import os

wit_access_token = os.environ["WIT_ACCESS_TOKEN"]

def parse_request(request_text):

    client = Wit(wit_access_token)
    response = client.message(request_text)
    # intent is a list, in which the second element is the confidence (0-1)
    entities = response.get('entities')

    intent = ''
    if 'duration' in entities:
        duration_seconds = entities['duration'][0]['normalized']['value']
        # because there are 48 blocks, each block is 30 minutes
        duration_blocks = int(duration_seconds / (30 * 60))
        duration = duration_blocks
        intent = 'duration_set'
    elif 'intent' in entities:
        intent = entities.get('intent')[0].get('value')
    elif 'datetime' in entities:
        try:
            datetime = entities['datetime'][0]['value']
        except Exception:
            print(entities['datetime'][0])
            raise KeyError
        intent = 'date_set'
    elif 'identify' in entities:
        name = entities['identify'][0]['value']
        intent = 'identify'
    # the intended action will be stored here
    action = ''
    info = None

    if (intent == 'meeting_set'):
        action = 'schedule'
    elif (intent == 'yes'):
        action = 'accept'
    elif (intent == 'no'):
        action = 'reject'
    elif (intent == 'duration_set'):
        action = 'set_duration'
        info = duration
    elif (intent == 'date_set'):
        action = 'set_date'
        info = datetime
    elif (intent == 'identify'):
        action = 'identify'
        info = name
    else:
        print('no action found for intent {}'.format(intent))
        action = None

    return (action, info)
