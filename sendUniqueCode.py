import random
import string
import os
import callscripts
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

def generatePinCode():
    code=[]
    for x in range(0, 5):
        if x != 4:
            code.append(random.randint(0, 9))
    generatedCode = ''.join( map(str , code))
    return generatedCode

def sendCodeToUser(userPhoneNumber):
    code = generatePinCode()
    message =  client.api.account.messages.create(
      to=userPhoneNumber,
      from_= os.environ["ALFRED_BETA_PHONE_NUMBER"],
      body= "Hi to access the meeting that you booked with Mr." +  callscripts.UserName  + ",use this pin code " + code)
    return code


generatePinCode()
