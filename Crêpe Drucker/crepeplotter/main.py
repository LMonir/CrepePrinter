#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxClient, LogicMailbox
import usocket as socket
import json
from printer import Printer

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

CONTENT = b"""\
HTTP/1.0 200 OK

Hello #%d from MicroPython!
"""

# Create your objects here.
ev3 = EV3Brick()
client = BluetoothMailboxClient()
client.connect('ev3_5')
mail = LogicMailbox('print', client)

ev3.light.on(Color.RED)
ev3.screen.clear()
ev3.screen.print('CALIBRATING.', sep=' ', end='\n')

mail.send(False)
mail.wait()
print(mail.read())
wait(1000)
mail.send(True)
mail.wait()
print(mail.read())
wait(1000)
mail.send(False)
mail.wait()
print(mail.read())
# Write your program here.
ev3.speaker.beep()

printer = Printer(ev3)
printer.calibrate()

ev3.speaker.beep()
wait(100)
ev3.speaker.beep()

ev3.light.on(Color.GREEN)
ev3.screen.clear()

# Define the server's host and port
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 8080

s = socket.socket()

# Binding to all interfaces - server will be accessible to other hosts!
ai = socket.getaddrinfo(HOST, PORT)
print("Bind address info:", ai)
addr = ai[0][-1]

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)
print("Listening, connect your browser to http://<this_host>:80/")

# Listen for incoming connections
s.listen(1)

print('Server is listening on {}:{}'.format(HOST, PORT))
ev3.screen.clear()
ev3.screen.print('Please upload a\npicture for\nprinting.', sep=' ', end='\n')
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
        print(h)5
    '''

    data = client_sock.recv(1024)  # Receive up to 1024 bytes of data
    if data:
        decoded_data = data.decode('utf-8')
        print('Received data: {}'.format(decoded_data))
        lines = decoded_data.split("\r\n")
        anz_lines = len(lines)
        content = lines[anz_lines-1]
        json_object = json.loads(content)
        print(json_object)
        client_sock.write(CONTENT % counter)
        client_sock.close()

        '''
        gcodes = json_object['gcodes']
        
        '''
        ev3.light.on(Color.RED)
        ev3.screen.clear()
        ev3.screen.print('Printing!!!\nPlease stay back!.', sep=' ', end='\n')

        mail.send(True)
        mail.wait()
        print(mail.read())

        wait(2000)
        ev3.speaker.beep()
        wait(100)
        ev3.speaker.beep()
        wait(100)
        ev3.speaker.beep()
        printer.runGCode(json_object['ip'], int(json_object['port']))
        printer.calibrate()

        mail.send(False)
        mail.wait()
        print(mail.read())

        ev3.light.on(Color.GREEN)
        ev3.screen.clear()
        ev3.screen.print('Your crepe is\nready to eat.\n\nUpload a new\npicture.', sep=' ', end='\n')
        #client_sock.send(response.encode('utf-8'))
        
    counter += 1
    print()

# Close the server socket
s.close()
