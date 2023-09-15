#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import usocket as socket
import json

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

CONTENT = b"""\
HTTP/1.0 200 OK

Hello #%d from MicroPython!
"""

# Create your objects here.
ev3 = EV3Brick()

# Write your program here.
ev3.speaker.beep()

# Define the server's host and port
HOST = ''  # Listen on all available interfaces
PORT = 80

s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
ai = socket.getaddrinfo("0.0.0.0", 8080)
print("Bind address info:", ai)
addr = ai[0][-1]

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)
print("Listening, connect your browser to http://<this_host>:8080/")

# Listen for incoming connections
s.listen(1)

print('Server is listening on {}:{}'.format(HOST, PORT))

counter = 0
while True:
    res = s.accept()
    client_sock = res[0]
    client_addr = res[1]
    print("Client address:", client_addr)
    print("Client socket:", client_sock)

    '''
    print("Request:")
    req = client_stream.readline()
    print(req)
    while True:
        h = client_stream.readline()
        if h == b'':
            break
        print(h)
    '''

    data = client_sock.recv(1024)  # Receive up to 1024 bytes of data
    if data:
        decoded_data = data.decode('utf-8')
        #print('Received data: {}'.format(decoded_data))
        lines = decoded_data.split("\r\n")
        anz_lines = len(lines)
        content = lines[anz_lines-1]
        json_object = json.loads(content)
        gcodes = json_object['gcodes']
        for e in gcodes:
            print(e)
        #client_sock.send(response.encode('utf-8'))
        client_sock.write(CONTENT % counter)

    client_sock.close()
    counter += 1
    print()

# Close the server socket
s.close()
