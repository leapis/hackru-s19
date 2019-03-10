from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
from subprocess import Popen, PIPE
import redis
import json
import encode

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
        print("Error Reported From NodeJs Script")
        echo.message(txtnumbers)
    else:
        decodedtxt = txtnumbers.decode("utf-8")
        databasekey = decodedtxt.split(" ",1)[0]
        pagename = decodedtxt.split(" ",1)[1]
        print("Database Key: "+databasekey)
        print("Page Name: "+pagename) 


        jsontable = redistojson(databasekey, pagename)        

        print(jsontable)

        echo.message(databasekey+"\n"+pagename)

    return(str(echo))


def urltopng(url):
    if (not url.startswith("http")):
            url = "http://"+url

    print(url)

    output = Popen(["node","get_site/index.js",url], stdout=PIPE, stderr=PIPE)

    stdout = output.communicate()[0]
    print(output.returncode)
    if(output.returncode == 1):
            return "error"

    return stdout


def redistojson(key, title):
    conn = redis.from_url("redis://redis:6379/0")
    conn = redis.StrictRedis(
        host="redis",
        port=6379,
        charset="utf-8",
        decode_responses=True,
    )
    jsontable = {}
    jsontable["title"] = title
    jsontable["links"] = conn.get("%s:*" % key) 

    encode.compress(jsontable, conn.get(key))

    return json.dumps(jsontable)





















