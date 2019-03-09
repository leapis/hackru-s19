from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Clien

client = Client('AC1519f6c35abae292854d60746394de52', '48e3893e7ad7e865b6893ba175160fe4')
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/sms', methods=['POST'])
def textfrom():
    echo = MessagingResponse()

    echo = request.form['Body']

    response.message(echo)

    return(str(response))

