import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage

def on_button1_click():
    # Hier wird Ihre Logik für den ersten Button ausgeführt
    print("Button 1 clicked")

def on_button2_click():
    # Hier wird Ihre Logik für den zweiten Button ausgeführt
    print("Button 2 clicked")


# Laden Sie das Bild
file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
image = cv2.imread(file_path)

# Konvertieren Sie das Bild in Graustufen
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Anwenden eines Glättungsoperators, um Rauschen zu reduzieren (optional)
blurred = cv2.GaussianBlur(gray, (5, 5), 0, borderType=cv2.BORDER_REPLICATE)

# Kanten erkennen
edges = cv2.Canny(blurred, 50, 150)

# Konturen finden
contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Erstellen Sie ein leeres Bild zum Zeichnen der vereinfachten Darstellung
simplified_image = np.zeros_like(image)

# Zeichnen Sie die vereinfachten Darstellungen der Konturen auf das Bild
for contour in contours:
    simplified_image = np.zeros_like(image)
    area = cv2.contourArea(contour)
    # Approximieren Sie die Kontur mit einer Polygonzugkurve
    epsilon = 0.005 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Zeichnen Sie die vereinfachte Kontur als Linie oder Polygon auf das Bild
    cv2.drawContours(simplified_image, [approx], 0, (255, 255, 255), 1)
    height, width, channels = simplified_image.shape
    tk_image = PhotoImage(width=width, height=height)
    tk_image.put("{RGB} " + " ".join(map(str, image.flatten())))

# Anzeigen des Originalbildes und des vereinfachten Bildes
cv2.imshow('Simplified Image', simplified_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

def show_image():
    # Erstellen Sie ein Tkinter-Fenster
    window = tk.Tk()

    # Bild anzeigen
    label = tk.Label(window, image=tk_image)
    label.pack()

    # Erstellen Sie Schaltflächen
    button1 = tk.Button(window, text="Button 1", command=on_button1_click)
    button1.pack(side=tk.LEFT)
    
    button2 = tk.Button(window, text="Button 2", command=on_button2_click)
    button2.pack(side=tk.RIGHT)

    # Tkinter Hauptloop starten
    window.mainloop()

# Funktion zum Anzeigen des vereinfachten Bildes
def show_simplified_image():
    # ... (Ihr vereinfachter Bildcode hier)

# Rufen Sie die Funktion show_image auf
show_image()