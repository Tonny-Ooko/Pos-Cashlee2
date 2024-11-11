from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

account_sid = 'ACe140beae8b884f7056dc35b0ef15c7b4'
auth_token = '77377fb40f7f363a600aaf0127d451aa'
client = Client(account_sid, auth_token)

twilio_phone_number = '+254 705 598269'
destination_phone_number = '+1 972-360-9222'
message_body = 'Activate'

try:
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=destination_phone_number
    )
    print(f'Message sent with SID: {message.sid}')
except TwilioRestException as e:
    print(f'Error sending message: {e}')

