import socket

import socket
import json

class SocketClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

    def send_http_request(self, method, path=None, headers=None, body=None):
        try:
            # Verbindung zum Server herstellen
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.server_address, self.server_port))

                # HTTP-Request erstellen
                request_headers = f"{method} {path} HTTP/1.1\r\n"
                if headers:
                    for key, value in headers.items():
                        request_headers += f"{key}: {value}\r\n"

                if body:
                    body_json = json.dumps(body)
                    request_headers += f"Content-Length: {len(body_json)}\r\n"
                    request_headers += "Content-Type: application/json\r\n"

                # HTTP-Request senden
                request = f"{request_headers}\r\n"
                if body:
                    request += f"{body_json}\r\n"

                client_socket.send(request.encode())

                # Serverantwort empfangen und ausgeben
                response = client_socket.recv(1024)
                print(response.decode())

        except Exception as e:
            print(f"Fehler beim Senden des HTTP-Requests: {e}")

if __name__ == "__main__":
    # Beispielverwendung der SocketClient-Klasse
    server_address = "example.com"  # Hier die Serveradresse eintragen
    server_port = 80  # Hier den Port eintragen

    client = SocketClient(server_address, server_port)

    # Beispiel-HTTP-Request
    request_method = "GET"
    request_path = "/api/resource"
    request_headers = {
        "Host": server_address,
        "User-Agent": "SocketClient",
    }
    request_body = {
        "key": "value",
    }

    client.send_http_request(request_method, request_path, request_headers, request_body)
