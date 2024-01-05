import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from tkinter import filedialog
import numpy as np
from Server import Server
from GCodeGenerator import GCodeGenerator
import os

class ImageGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Grid App")
        self.images = []
        self.contours = []
        self.image_state = []
        self.server = Server()
        self.epsilon = 0.007

        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        file_path = os.path.abspath(file_path)
        self.image = cv2.imread(file_path)

        # Konvertieren Sie das Bild in Graustufen
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Anwenden eines Glättungsoperators, um Rauschen zu reduzieren (optional)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0, borderType=cv2.BORDER_REPLICATE)

        # Kanten erkennen
        edges = cv2.Canny(blurred, 50, 150)

        # Konturen finden
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = contours

        # Erstellen Sie ein leeres Bild zum Zeichnen der vereinfachten Darstellung
        simplified_image = np.zeros_like(self.image)

        # Zeichnen Sie die vereinfachten Darstellungen der Konturen auf das Bild
        for contour in contours:
            simplified_image = np.zeros_like(self.image)
            area = cv2.contourArea(contour)
            # Approximieren Sie die Kontur mit einer Polygonzugkurve
            epsilon = self.epsilon * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Zeichnen Sie die vereinfachte Kontur als Linie oder Polygon auf das Bild
            cv2.drawContours(simplified_image, [approx], 0, (255, 255, 255), 2)
            pil_image = Image.fromarray(cv2.cvtColor(simplified_image, cv2.COLOR_BGR2RGB))
            tk_image = ImageTk.PhotoImage(pil_image)
            self.images.append(tk_image)

        self.num_images = len(contours)
        
        # Erstellen Sie ein leeres Dictionary für die Image-Labels und die Bildvariablen
        self.image_labels = {}
        self.image_vars = {}

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Erstellen Sie eine Scrollbar und binden Sie sie an das Canvas
        self.scrollbar = tk.Scrollbar(self.root, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Raster erstellen
        self.create_grid()

        # Konfigurieren Sie das Canvas, um auf Größenänderungen zu reagieren
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        # Binden Sie das Mausrad-Ereignis zum Scrollen
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)

    def create_grid(self):
        self.grid_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor='nw')
        self.grid_frame.bind('<MouseWheel>', self.on_mouse_wheel)
        for i in range(self.num_images):
            tk_image = self.images[i]

            # Erstellen Sie eine Bildvariable und fügen Sie sie dem Dictionary hinzu
            image_var = tk.StringVar()
            self.image_vars[i] = image_var

            # Erstellen Sie ein Label mit dem Bild und fügen Sie es dem Dictionary hinzu
            image_label = tk.Label(self.grid_frame, image=tk_image, textvariable=image_var, compound='top')
            image_label.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            image_label.bind('<MouseWheel>', self.on_mouse_wheel)
            self.image_labels[i] = image_label

            # Fügen Sie das Bild in das Label ein
            image_var.set(tk_image)

            # Binden Sie die Klickaktion an das Bild
            image_label.bind('<Button-1>', lambda event, idx=i: self.on_image_click(idx))
            self.image_state.append(False)
        
        print_button = tk.Button(self.grid_frame, text="Auswahl angucken", command=self.auswahl_angucken)
        print_button.grid(row=self.num_images // 4, column=0, columnspan=2, pady=10)
        print_button = tk.Button(self.grid_frame, text="Drucken", command=self.print_images)
        print_button.grid(row=self.num_images // 4, column=0, columnspan=5, pady=10)

    def on_image_click(self, idx):
        # Hier können Sie Ihre Aktionen für das Bild beim Klicken ausführen
        # Zum Beispiel die grüne Umrandung hinzufügen
        if not self.image_state[idx]:
            self.image_labels[idx].configure(borderwidth=5, relief="solid", highlightbackground="black")
            self.image_state[idx] = True
        else:
            self.image_labels[idx].configure(borderwidth=0)
            self.image_state[idx] = False

    def on_canvas_configure(self, event):
        # Passen Sie die Scrollregion des Canvas an die Größe des Rasters an
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def on_mouse_wheel(self, event):
        # Scrollen Sie mit dem Mausrad im Canvas
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def auswahl_angucken(self):
        simplified_image = np.zeros_like(self.image)
        for i in range(self.num_images):
            if self.image_state[i]:
                contour = self.contours[i]
                area = cv2.contourArea(contour)
                # Approximieren Sie die Kontur mit einer Polygonzugkurve
                epsilon = self.epsilon * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                # Zeichnen Sie die vereinfachte Kontur als Linie oder Polygon auf das Bild
                cv2.drawContours(simplified_image, [approx], 0, (255, 255, 255), 2)

        # Anzeigen des Originalbildes und des vereinfachten Bildes
        cv2.imshow('Simplified Image', simplified_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def print_images(self):
        gcodes = []
        gcodeGenerator = GCodeGenerator()
        for i in range(self.num_images):
            if self.image_state[i]:
                contour = self.contours[i]
                gcode = gcodeGenerator.generateGCodeVectorized(contour)
                gcodes = gcodes + gcode
        print(gcodes)
        self.server.start_printing(gcodes)

        

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGridApp(root)
    root.mainloop()