import usocket as socket
import json

class SocketClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def next(self):
        s = socket.socket()
        ai = socket.getaddrinfo(self.ip, self.port)
        print("Address infos:", ai)
        addr = ai[0][-1]

        print("Connect address:", addr)
        s.connect(addr)
        s.send(b"GET / HTTP/1.0\r\n\r\n")
        data = s.read()
        decoded_data = data.decode('utf-8')
        print('Received data: {}'.format(decoded_data))
        lines = decoded_data.split("\r\n")
        anz_lines = len(lines)
        content = lines[anz_lines-1]
        json_object = json.loads(content)
        gcodes = json_object['gcodes']
        s.close()
        return gcodes
