from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
from subprocess import Popen, PIPE
import redis
import json
import encode
from textwrap import wrap



client = Client('AC4f12756b126ebd6aa4153488daf82495', '15640a307f38d8f85ee6e8284937ef1d')
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
        

        #variable for max message size
        n = 1500

        splittable = [jsontable[i:i+n] for i in range(0, len(jsontable), n)]

        print(splittable)

        message = client.messages \
            .create(
                 body='#0000%04d' % len(splittable)+splittable[0],
                 from_='+18332598513',
                 to='+18337131276'
             )

        msgcounter = 1

        for string in splittable[1:]:
            message = client.messages \
                .create(
                     body='%04d' % msgcounter + string,
                     from_='+18332598513',
                     to='+18337131276'
                 )
            msgcounter = msgcounter + 1

        print(len(splittable)) 
        print(message.body)
        print(len(jsontable))


    return(jsontable)


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





















