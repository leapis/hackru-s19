import multiprocessing
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
from multiprocessing import Process, Queue

def output(q):
    import socket
    from receiver import Receiver

    HOST = '127.0.0.1'
    PORT = 5558 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(4)

    while True:
        Receiver(s.accept(), q).start()

def input(q):
    from emulator import Emulator
    import json
    import math

    while True:
        text = q.get(True)
        print(text)

        emulator = Emulator(5554)

        pages = math.ceil(len(text) / 1500.0)
        counter = 0
        texts = []
        while len(text) > 0:
            t = "%04d" % counter
            if counter == 0:
                t = "#%04d%04d" % (counter, pages - 1)
            counter += 1
            texts.append(t + text[:1500])
            text = text[1500:]
            if counter >= pages:
                break

        for text in texts:  
            emulator.send_sms("6666", text)

if __name__ == "__main__":

    # from emulator import Emulator
    # import json
    # emulator = Emulator(5554)
    # text = json.dumps({"i": open("test.txt", "r").read()})

    # import math
    # pages = math.ceil(len(text) / 1500.0)
    # counter = 0
    # texts = []
    # while len(text) > 0:
    #     t = "%04d" % counter
    #     if counter == 0:
    #         t = "#%04d%04d" % (counter, pages - 1)
    #     counter += 1
    #     texts.append(t + text[:1500])
    #     text = text[1500:]
    #     if counter >= pages:
    #         break

    # for text in texts:  
    #     emulator.send_sms("6666", text)

    # exit()

    q = Queue()
    p_input = multiprocessing.Process(target=input, args=(q,))
    p_output = multiprocessing.Process(target=output, args=(q,))
    p_input.start()
    p_output.start()

    p_input.join()
    p_output.join()

