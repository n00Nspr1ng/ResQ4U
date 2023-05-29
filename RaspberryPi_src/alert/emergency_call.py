# Code for Emergency Call
from common.imports import *


class EmergencyCaller():
    def __init__(self):
        self.account_sid = 'type dahyun sid' # dahyun account.. will be used
        self.auth_token = 'type dahyun token'
        self.resq4u_number = '+13159225838' # fraud number (just to make calls)
        self.recipient_number = '+821090531622' # dahyun phone number
        
    def callHELP(self):
        # Create client
        client = Client(account_sid, auth_token)

        # Create call from created client & req. url
        call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to=recipient_number,
            from_=twilio_number
        )
        print('Calling Dahyun')
        print('SID Log: 'call.sid)
        
if __name__ == '__main__':
    caller = EmergencyCaller()
    caller.callHELP()
