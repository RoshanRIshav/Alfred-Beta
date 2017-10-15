# Alfred- Beta v0.1

# Who is Alfred?
Alfred is a smart bot, that lives on a phone number, yes a phone number. Currently in its beta version, it has the capability to schedule meetings for its owner, and populate the owners google calendar accordingly.

# How can someone book a meeting?
Booking meetings using alfred is super simple and easy. All you have to do is call alfred on its phone number, state your name, reason for the meeting, time for the meeting and the location, and that's it. If the owner is free at the specified time, the meeting will be booked and you will be provided with a four digit pin, that can give you access to delete/cancel your meeting.

# How does it work?

The whole codebase for Alfred is written in python. Every user who wants to sign up for a personal assistant, have to sign up using their google account, and give alfred the access to their google calendar. Once done, the user will be provided with a twilio phone number which will be the access point for their own personal Alfred. 

# What to expect in the future?

Currently, Alfred is in its very initial stage, and has a lot of features that are going to be added to it. 
The features will be:
1. Multiple user support.
2. Event editing support.
3. Personal goals/tasks support.
4. NLP implementation so that the conversations with Alfred would be much better then it is currently.
5. Analytics support, to get an insight about what type of meetings/appointments are usually booked.
6. Workspace support: Alfred for every employee in your company.
7. Full customization for the conversation.

# How is the code structured?

I have tried to segregate the code into very several modules to reduce coupling, and the code should be very straight forward to follow.
The main files are:
1. incomingCalls.py : it handles the call script which is how alfred knows what and how to speak.
2. brain.py : it handles the NLP (** currently it only supports multiple date/time formats ** )
3. makeEvent.py : it deals with the google calendar service and has the functions to create/cancel the events.
4. sendUniqueCode.py : it generates a unique code for every appointment, and it is sent to the person who was booking the meeting/appointment, enabling them to cancel their event.

For more insight, the routes in the incomingCalls.py file is designed using the following flowchart:
https://imgur.com/PWJiMnr
