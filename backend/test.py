from twilio.rest import Client

client = Client('AC1519f6c35abae292854d60746394de52', '48e3893e7ad7e865b6893ba175160fe4')

message = client.messages \
                .create(
                     body="HELLO",
                     from_='+16149831295',
                     to='+19087237082'
                 )

print(message.sid)
