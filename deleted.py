# mongo = PyMongo(app)
# connection = MongoClient("mongodb://ds147544.mlab.com:47544/")
# db = connection["userdatabase"]
# event_ID = db.event_ID
# db.authenticate(name="nikosm",password="Netherlands1")
# # Account SID and


#def addEventIDtoDatabase(eventID, eventCode):
#	eventCode=[("eventCode",eventCode)]
#	eventID=[("event_ID",eventID)]
#	a={}
#	a.update(eventCode)
#	a.update(eventID)
#	event_ID.insert_one(a)
#
#def deleteEventIDfromDatabase(eventID):
#    try:
#        print("ID")
#        print(eventID)
#        deletedID = event_ID.delete_one({ "event_ID": eventID})
#        return "Deleted"
#    except Exception,e:
#        return "ERROR"
#
#def isThereIndex(index):
#	x=event_ID.find_one({ "eventCode": index})
#	if x is not None:
#		print(1)
#		return x["event_ID"]
#	else:
#		print(0)
#		return None
#

#@app.route("/menu", methods=['GET', 'POST'])
#def menu():
#    resp = VoiceResponse()
#    gatherOption = Gather(num_digits=1, action='/decider')
#    gatherOption.say("Hi this is Alfred, Press zero, if you want to create a new event, or press 1 if you want to access an old event ")
#    resp.append(gatherOption)
#    # Start our <Gather> verb
#
#    # If the user doesn't select an option, redirect them into a loop
#    resp.redirect('/voice')
#    return str(resp)
#
#@app.route("/decider", methods=['GET', 'POST'])
#def decider():
#    resp = VoiceResponse()
#    if "Digits" in request.values:
#        if request.values["Digits"] == '1':
#            gather = Gather(num_digits=5, action='/cancelEvent')
#            gather.say("Press your event code")
#            resp.append(gather)
#            return str(resp)
#        else:
#            resp.redirect('/voice')
#            return str(resp)
#
#@app.route("/cancelEvent", methods=['GET', 'POST'])
#def cancelEvent():
#    resp = VoiceResponse()
#    if "Digits" in request.values:
#        pin = request.values["Digits"]
#        eventId = isThereIndex(pin)
#        print(eventId)
#        if eventId != "None":
#            done = makeEvent.cancel_event(eventId)
#            if done == "Cancelled":
#                x=deleteEventIDfromDatabase(eventId)
#                print(x)
#                resp.say("Your event has been cancelled, Have a good day, Bye now!")
#                return str(resp)
#            else:
#                resp.say("It seems that there is no event associated with this pin, Please wait while you are taken back to the main menu")
#                resp.redirect('decider')
#        else:
#            resp.say("It seems that there is no event associated with this pin, Please wait while you are taken back to the main menu")
#            resp.redirect('decider')

# @app.route('/getSuggestion', methods=['GET', 'POST'])
# def getSuggestion():
#     resp = VoiceResponse()
#     if 'SpeechResult' in request.values:
#         needSuggestion = request.values['SpeechResult']
#         if (needSuggestion == "Yes.") or (needSuggestion == "Yes") or (needSuggestion == "yes." or (needSuggestion == "yes") or (needSuggestion == "sure"))  :
#             hasPickedDay=False
#             #schedule=Schedule()
#             schedDict=makeEvent.fourteen_day_schedule()
#             schedule = makeEvent.convert_time_to_block(schedDict)
#             sched=Schedule()
#             utc_datetime = datetime.datetime.utcnow()
#             currentTime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
#             time_now = makeEvent.convert_input_time_to_block(currentTime)
#
#             # # fill the schedule with the schedule downloaded from GCalendar
#             organizing_data = organizing_data_helper.get_default()
#             # # fill the organizing_data with the event data that we have
#             # time_now = (0, 0)# WRONG, should have current time
#             # meeting_duration = 1 #WRONG, should contain meeting duration
#             print("hello")
#             suggested_time = suggest_time(
#              sched, time_now, organizing_data, 1)
#             day, block=suggested_time
#             print(day)
#             print(block)
#             enDate= day_block_to_date_string((day,block+2))
#             starDate=day_block_to_date_string((day,block))
#             print('A suggested date is '+str(starDate))
#             resp.say("A suggested date is "+str(starDate))
#             gather = Gather(input='speech dtmf', action='/bookOrNot')
#             gather.say("Is this time ok with you?")
#             resp.append(gather)
#             return str(resp)
