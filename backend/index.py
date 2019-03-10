from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
from subprocess import Popen, PIPE


client = Client('AC1519f6c35abae292854d60746394de52', '48e3893e7ad7e865b6893ba175160fe4')
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/sms', methods=['POST','GET'])
def textfrom():

    body = request.values.get('Body', None)
    
    #Where the URL should come in at
    txtnumbers = urltopng(body)

    print(txtnumbers)

    echo = MessagingResponse()

    if(txtnumbers == "error"):
        echo.message(txtnumbers)
    else:
        echo.message(txtnumbers.decode("utf-8"))

    return(str(echo))


def urltopng(url):
    if (not url.startswith("http://") or not url.startswith("https://")):
            url = "http://"+url

    output = Popen(["node","get_site/index.js",url], stdout=PIPE, stderr=PIPE)

    stdout = output.communicate()[0]
    print(output.returncode)
    if(output.returncode == 1):
            return "error"

    return stdout

   # return "HELLO" 

