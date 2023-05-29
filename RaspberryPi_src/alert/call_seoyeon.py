# Code for Emergency Call
from common.imports import *

# Account info..
account_sid = 'type dahyun sid' # dahyun account.. will be used
auth_token = 'type dahyun token'
twilio_number = '+13159225838'
recipient_number = '+821090531622' # dahyun phone num for test ,,,,

# Create client
client = Client(account_sid, auth_token)

# Create call from created client & req. url
call = client.calls.create(
    url='http://demo.twilio.com/docs/voice.xml',
    to=recipient_number,
    from_=twilio_number
)

# After making call, print SID log in terminal
print(call.sid)
