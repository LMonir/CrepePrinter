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

def get_next_10_entries(array, current_index):
    # Überprüfe, ob der aktuelle Index im gültigen Bereich des Arrays liegt
    if current_index < len(array):
        # Berechne den Endindex für die nächsten 10 Einträge
        end_index = min(current_index + 10, len(array))
        
        # Holen Sie die nächsten 10 Einträge aus dem Array
        next_10_entries = array[current_index:end_index]
        
        # Aktualisiere den aktuellen Index für den nächsten Aufruf
        current_index = end_index
        
        return next_10_entries, current_index
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
        next_10, current_index = get_next_10_entries(gcodes, current_index)

        if next_10:
            # Erstelle ein JSON-Datenobjekt
            data = {'gcodes': next_10}
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
        print(json_data)
        self.wfile.write(json_data.encode('utf-8'))
        if not next_10:
            thread = threading.Thread(target=worker_function, args=(server,))
            thread.start()


class SocketServer:
    def __init__(self, gcodess):
        global gcodes
        global server
        gcodes = gcodess
        with socketserver.TCPServer(('', 80), MyHandler) as httpd:
            print('Der Server läuft auf Port 80...')
            server = httpd
            # Starte den Server
            httpd.serve_forever()


