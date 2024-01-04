from bluetooth_client import SocketClient
from SocketServer import SocketServer
import sys

MAX_PIXEL = 202
IP_ROBOTER = "169.254.156.43"
IP_BT = "192.168.178.51"
IP_WLAN = "192.168.178.48"
sys.setrecursionlimit(32450)

class Server:
    def __init__(self):
        global MAX_PIXEL
        global IP_ROBOTER
        self.roboter = SocketClient(IP_ROBOTER, 8080)
        self.server = None
        
    def get_own_ip(self):
        global IP_WLAN
        global IP_BT
        return IP_WLAN
    
    def start_printing(self, gcodes):
        json_object = {
            'ip': self.get_own_ip(),
            'port': 8080
        }

        print(json_object)
        self.roboter.send_http_request("POST", body=json_object)

        print(gcodes)
        self.server = SocketServer(gcodes)