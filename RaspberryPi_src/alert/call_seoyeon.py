# Code for Emergency Call

# Account info..
account_sid = 'ACb9b1f9a5734af366c962dc679fecb4a7' # dahyun account.. will be used
auth_token = 'b3f435c08897918d7570d5d9586d90ff'
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
