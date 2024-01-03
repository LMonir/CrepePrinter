import math
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from bluetooth_client import SocketClient
from SocketServer import SocketServer
import socket
import sys

MAX_PIXEL = 202
roboter = SocketClient("169.254.156.43", 8080)
gcodes = []
printing = False
sys.setrecursionlimit(32450)

def get_own_ip():
    return "192.168.178.48"  #WLAN
    #return "192.168.178.51" Bluetooth

# Laden Sie das Bild ausgewählt durch den Benutzer
def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
    if file_path:
        image = Image.open(file_path)
        process_image(image)

def getNodesAround(image, x, y):
    point = (x, y)
    nodes = []
    for i in range(x-1, x+2, 1):
        for j in range(y-1, y+2, 1):
            if i >= 0 and i < image.width and j >= 0 and j < image.height:
                point2 = (i, j)
                if point != point2:
                    pixel = image.getpixel(point2)
                    if is_black(pixel):
                        nodes.append(str(i) + "_" + str(j))
    return nodes

def generateGraf(image):
    graph = {}
    nodes = []
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            if is_black(pixel):
                r = math.sqrt((x - MAX_PIXEL/2)**2 + (y - MAX_PIXEL/2)**2)
                if r > MAX_PIXEL/2:
                    raise Exception(f"Der Punkt({x}, {y}) befindet sich außerhalb des erlaubten Druckbereichs!")
                node = str(x) + "_" + str(y)
                nodes.append(node)
                graph[node] = getNodesAround(image, x, y)

    return graph, nodes

def dfs(graph, node, visited):
    global printing
    global gcodes
    if node not in visited:
        spl = node.split("_")
        gcodes.append(create_gcode(spl[0], spl[1]))
        if not printing:
            gcodes.append("G2 1")
            gcodes.append("G3 200")
            printing = True
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(graph, neighbor, visited)
                if printing:
                    gcodes.append("G2 0")
                    printing = False


# Überprüfen Sie die Bildgröße und verarbeiten Sie es zeilenweise
def process_image(image):
    if image.size != (MAX_PIXEL, MAX_PIXEL):
        raise Exception(f"Das Bild muss {MAX_PIXEL}x{MAX_PIXEL} Pixel groß sein.")
    
    graph, nodes = generateGraf(image)

    while len(nodes) > 0:
        visited = set()
        node = nodes[0]
        print(f"Start Graph with node: {node}")
        dfs(graph, node, visited)
        nodes = [x for x in nodes if x not in visited]
    
    json_object = {
        'ip': get_own_ip(),
        'port': 8080
    }
    print(json_object)
    roboter.send_http_request("POST", body=json_object)

    print(gcodes)
    server = SocketServer(gcodes)

# Überprüfen, ob ein Pixel schwarz ist (R, G, B = 0)
def is_black(pixel):
    return pixel == (0, 0, 0) or pixel == (0, 0, 0, 255)

# Erstellen Sie einen vereinfachten GCode-Befehl für ein schwarzes Pixel
def create_gcode(x, y):
    return f"G1 {x} {y}"  # Hier können Sie Ihren GCode anpassen, je nach Bedarf

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Verstecken Sie das Hauptfenster von tkinter
    while True:
        print("Bitte wählen Sie ein Bild aus:")
        load_image()


#G1 ist ein Move Befehl
#G2 ist ein Druckbefehl 0 = False, 1 = True
#G3 ist ein Warte Befehl in ms