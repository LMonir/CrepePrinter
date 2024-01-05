import http.server
import socketserver
import json
import threading
import time

current_index = 0
gcodes = None
server = None

def worker_function(ser):
    time.sleep(3)
    print("BEENDE DEN SERVER")
    ser.shutdown()

def get_next_X_entries(array, current_index):
    arraylengh = len(array)
    # Überprüfe, ob der aktuelle Index im gültigen Bereich des Arrays liegt
    print(f"[{current_index}/{arraylengh}]")
    if current_index < arraylengh:
        # Berechne den Endindex für die nächsten X Einträge
        end_index = min(current_index + 30, arraylengh)
        
        # Holen Sie die nächsten X Einträge aus dem Array
        next_X_entries = array[current_index:end_index]
        
        # Aktualisiere den aktuellen Index für den nächsten Aufruf
        current_index = end_index
        
        return next_X_entries, current_index
    else:
        # Wenn der aktuelle Index außerhalb des Arrays liegt, gib None zurück
        return None, current_index

# Definiere die Handler-Klasse
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global current_index
        global server
        global gcodes
        global pool
        next_X, current_index = get_next_X_entries(gcodes, current_index)

        if next_X:
            # Erstelle ein JSON-Datenobjekt
            data = {'gcodes': next_X}
            json_data = json.dumps(data)

            # Setze den Content-Type auf JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        else:
            print("ENDE")
            data = {'gcodes': ["G4"]}
            json_data = json.dumps(data)

        # Sende das JSON als Antwort
        self.wfile.write(json_data.encode('utf-8'))
        if not next_X:
            thread = threading.Thread(target=worker_function, args=(server,))
            thread.start()


class SocketServer:
    def __init__(self, gcodess):
        global gcodes
        global server
        gcodes = gcodess
        with socketserver.TCPServer(('', 8080), MyHandler) as httpd:
            print('Der Server läuft auf Port 80...')
            server = httpd
            # Starte den Server
            httpd.serve_forever()


