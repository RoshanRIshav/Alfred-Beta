import random
import string
import os
import callscripts
import database
from twilio.rest import Client

#TWILIO ACCOUNT DETAILS
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)
####

#A randomly generated pin code is generated
def generatePinCode():
    code=[]
    for x in range(0, 5):
        if x != 4:
            code.append(random.randint(0, 9))
    generatedCode = ''.join( map(str , code))
    return generatedCode

#the code generated from the generatePinCode() is sent to the caller using this function
def sendCodeToUser(userPhoneNumber):
    code = generatePinCode()
    message =  client.api.account.messages.create(
      to=userPhoneNumber,
      from_= os.environ["ALFRED_BETA_PHONE_NUMBER"],
      body= callscripts.SendUniqueCodeScript1 +  callscripts.UserName  + callscripts.SendUniqueCodeScript2 + code)
    return code


generatePinCode()
