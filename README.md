Won award for *Best Use of Google Cloud Platform*.

## Our Main Concept

Going into this project, we wanted to tackle a project that was both technically challenging
and that aimed to solve a social problem plaguing our world today. After researching topics
that could have solutions that lie within computer science, we found that it is estimated that
4.8 billion people are not connected to the internet and mobile phones are as common in South Africa 
as they are in the United States. This led us on a natural progression to the connecting these people
from their existing SMS textng plans onto the world wide web. Using Twilio's to send sms messages, we
developed an android mobile application that allows users to type in URL's and shortly later recieve
their desired webpage on their phone, thus connecting billions of more people into the cyberspace
that we take for granted.

## How It Works

The lifetime of this starts and begins with our mobile android application. The user submits a URL or
picks a cached URL from their personalized list of previous requests. Then using a Twilio phone number,
we send this url to a webhook on our Google Cloud Computing server. There the URL is parsed by a NodeJs
script utilizing a headless chrome instance to retrieve page metadata and an image of the page. This is 
all stored in an instance of a Redis database. From this point, the metadata is pulled out and run through our 
compression algorithim. This shrinks the image and metadata to be a reasonable size for transmission through
SMS protocol. This is then transported back to the sender through the Twilio API once again. The data is recieved
by the android mobile application and parsed back from the text compressed form to the image and metadata. This is 
then displayed for the user on the application. The user will be able to click on in page links on the image due to
the identification and sending of links in the image metadata from the server. 
