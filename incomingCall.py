import os
import random
import string
import callscripts
from sendUniqueCode import sendCodeToUser, generatePinCode
import makeEvent
from brain import parse_request
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import datetime
from math import floor



app = Flask(__name__)

# enDate = ""
# starDate = ""

#The Event template, which gets filled during the call
event = {
  'summary': '',
  'location': '',
  'description': '',
  'start': {
    'dateTime': '',
    'timeZone': 'America/New_York',
  },
  'end': {
    'dateTime': '',
    'timeZone': 'America/New_York',
  }
 }

#The CallScript starts
#All of the routes are both "GET" and "POST"
#GET when they are redirected to, and POST
#when a Gather is sent as data.
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()
    gatherName = Gather(input='speech dtmf', action='/summary')
    gatherName.say(callscripts.GreetingString)
    resp.say(callscripts.Thanks)
    resp.append(gatherName)
    resp.redirect('/voice')
    return str(resp)
#Alfred asks for the reason for the meeting
@app.route('/summary', methods=['GET', 'POST'])
def gather():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        name = request.values['SpeechResult']
        print("Name of the caller: " + name) #Check
        gatherSummary = Gather(input = 'speech dtmf', action='/location')
        gatherSummary.say("Hello " + name + callscripts.AskForReason)
        resp.append(gatherSummary)
        return str(resp)
    else:
        resp.redirect('/voice')

#Alfred asks for the location of the meeting
@app.route('/location', methods=['GET', 'POST'])
def location():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        sumLong = request.values['SpeechResult']
        print("Summary: " + sumLong)
        event['summary'] = sumLong #adding to the dict
        gatherLocation = Gather(input='speech dtmf', action='/startTime')
        gatherLocation.say(callscripts.AskLocation)
        resp.append(gatherLocation)
        return str(resp)
    else:
        resp.redirect('/location')

#Alfred asks for the start time of the meeting
@app.route('/startTime', methods=['GET', 'POST'])
def startTime():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        locationDet = request.values['SpeechResult']
        print("Location of the meeting: " + locationDet)
        event['location'] = locationDet #adding to the dict
        gatherStartTime = Gather(input='speech dtmf', action='/endTime')
        gatherStartTime.say(callscripts.AskForStartTime + callscripts.TimeTemplate)
        resp.append(gatherStartTime)
        return str(resp)
    else:
        resp.redirect('/endTime')

#Alfred asks for the end time of the meeting
@app.route('/endTime', methods=['GET', 'POST'])
def endTime():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        print("Start Time: " + request.values['SpeechResult'])
        startTimeDet = parse_request(request.values['SpeechResult'])
        event['start']['dateTime'] = startTimeDet[1] #adding to the dict
        gatherEndTime = Gather(input='speech dtmf', action='/bookMeeting')
        gatherEndTime.say(callscripts.AskForEndTime + callscripts.TimeTemplate)
        resp.append(gatherEndTime)
        return str(resp)
    else:
        resp.redirect('/endTime')

#Alfred checks with the calendar and books a meeting if possible,
#else it is redirected to the retry route
@app.route('/bookMeeting', methods=['GET', 'POST'])
def bookMeeting():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        endTimeDet =  parse_request(request.values['SpeechResult'])
        print("End Time: " + request.values['SpeechResult'])
        event['end']['dateTime'] = endTimeDet[1] #adding to the dict
        resp.say(callscripts.WaitWhileBooking)
        CalendarResponse = makeEvent.create_event(event)
        print(CalendarResponse)
        if CalendarResponse != 'Busy':
            code = sendCodeToUser(request.values['From'])
            eventId = CalendarResponse[0]
            resp.say(callscripts.MeetingBookedSuccess)
            return str(resp)
        else:
            gather = Gather(input='speech dtmf', action='/retry')
            gather.say(callscripts.UserBusyMessage)
            resp.append(gather)
            return str(resp)
            print(event)
    else:
        resp.say(callscripts.SomethingHappenedErr)
        resp.redirect('/endTime')
#Alfred redirects the caller to the startTime route
@app.route('/retry', methods=['GET', 'POST'])
def retry():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        yesOrNo = request.values['SpeechResult']
        if yesOrNo.lower() == "yes":
            res.redirect('/startTime')
        else :
            resp.say(callscripts.Bye)


if __name__ == "__main__":
    print(os.environ["USERNAMECURRENT"])
    app.run(debug=True)
