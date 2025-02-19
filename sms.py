from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


try:
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=destination_phone_number
    )
    print(f'Message sent with SID: {message.sid}')
except TwilioRestException as e:
    print(f'Error sending message: {e}')

