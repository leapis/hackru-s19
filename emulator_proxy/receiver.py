import re
import threading
import gsmmodem
import requests

lock = threading.Lock()
clients = []

pat = re.compile("pdu ([0-9a-z]+)")

class Receiver(threading.Thread):
    def __init__(self, package, q):
        socket, address = package
        threading.Thread.__init__(self)
        self.socket = socket
        self.address= address
        self.q = q

    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        print('%s:%s connected.' % self.address)
        while True:
            data = self.socket.recv(2048)
            try:
                data = data.decode("ascii")
            except:
                continue

            match = pat.search(data)
            if match is None:
                continue

            encoded = match.group(1)
            decoded_data = gsmmodem.pdu.decodeSmsPdu(encoded)
            decoded = decoded_data["text"]
            
            print("waiting")
            response = requests.post("http://localhost/sms", data={"Body": decoded})
            print(response.status_code)
            if (response.status_code == 200):
                self.q.put(response.text)

        self.socket.close()
        print('%s:%s disconnected.' % self.address)
        lock.acquire()
        clients.remove(self)
        lock.release()