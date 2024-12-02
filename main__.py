import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.uic import loadUi
from main__get_coordinate_db import MapaAppGet

class CoordinateHandler(QObject):
    coordinatesReceived = pyqtSignal(list)  # Crear un nuevo signal

    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lon):
        print(f"Coordenadas clicadas: Latitud: {lat}, Longitud: {lon}")
        
        # Emitir las coordenadas para que sean manejadas por MapaApp
        self.coordinatesReceived.emit([lat, lon])

class MapaApp(QMainWindow):
    def __init__(self, latitud, longitud):
        super(MapaApp, self).__init__()
        loadUi("ui_mapa.ui", self)

        # Configuración del mapa
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mapa_html = os.path.join(current_dir, "mapa.html")
        url_base = QUrl.fromLocalFile(mapa_html)
        url_con_coordenadas = url_base.toString() + f"?lat={latitud}&lon={longitud}"
        self.channel = QWebChannel()
        self.coordinate_handler = CoordinateHandler()
        self.channel.registerObject("pyqtObj", self.coordinate_handler)
        self.webView.page().setWebChannel(self.channel)
        self.webView.setUrl(QUrl(url_con_coordenadas))

        # Campos de texto para mostrar las coordenadas
        self.lattxt = self.findChild(QLineEdit, "lattxt")
        self.lontxt = self.findChild(QLineEdit, "lontxt")
        
        if self.lattxt is None or self.lontxt is None:
            print("Error: No se encontraron los campos de texto 'lattxt' y 'lontxt'. Verifica los IDs en tu archivo .ui")
            return
        
        self.lattxt.setText("")
        self.lontxt.setText("")

        # Conectar la señal
        self.coordinate_handler.coordinatesReceived.connect(self.addCoordinate)

        # Conectar el botón
        self.btn_add.clicked.connect(self.triggerMessage)
        self.btn_get.clicked.connect(self.maps_get)

        # Almacenar todas las coordenadas
        self.coordinates = []

    def maps_get(self):
        self.latitud = -33.4569
        self.longitud = -70.6483
        self.window = MapaAppGet(self.latitud,self.longitud)
        self.window.show()

    @pyqtSlot(list)
    def addCoordinate(self, coordinates):
        self.coordinates.append({'lat': coordinates[0], 'long': coordinates[1]})
        self.saveCoordinates(coordinates)
        print(f"Coordenadas guardadas: Latitud: {coordinates[0]}, Longitud: {coordinates[1]}")  # Mostrar en print

    def updateTexts(self, lat, lon):
        self.lattxt.setText(f"{lat:.5f}")
        self.lontxt.setText(f"{lon:.5f}")

    def saveCoordinates(self, coordinates):
        # Actualizar los campos de texto con la nueva coordenada
        self.lattxt.setText(f"{coordinates[0]:.5f}")
        self.lontxt.setText(f"{coordinates[1]:.5f}")
        
        # Añadir nueva coordenada
        self.coordinates.append({'lat': coordinates[0], 'long': coordinates[1]})
        
        # Guardar todas las coordenadas en coordenadas_guardadas.json
        if self.coordinates:
            with open('coordenadas_guardadas.json', 'w') as f:
                json.dump(self.coordinates, f, indent=4)
            print("Coordenadas guardadas en coordenadas_guardadas.json")

    def triggerMessage(self):
        lat = float(self.lattxt.text())
        lon = float(self.lontxt.text())
        self.message(lat, lon)

    def message(self, lat, lon):
        print(f"Coordenadas clicadas: Latitud: {lat}, Longitud: {lon}")

        # Guardar la última coordenada en coordenada.json
        if os.path.exists('coordenada.json'):
            with open('coordenada.json', 'r') as f:
                existing_coordinates = json.load(f)
            if isinstance(existing_coordinates, dict):
                existing_coordinates = [existing_coordinates]  # Convertir dict en una lista si es necesario
        else:
            existing_coordinates = []

        color = "red"
        description = "cualquier cosa"
        status = "entregado"
        # Añadir nueva coordenada
        existing_coordinates.append({'latitude': lat, 'longitude': lon, 'color': color, 'description' : description, 'status' : status})

        # Guardar todas las coordenadas en coordenada.json
        with open('coordenada.json', 'w') as f:
            json.dump(existing_coordinates, f, indent=4)

        print("Última coordenada guardada en coordenada.json")


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    latitud = -33.4569
    longitud = -70.6483
    ventana = MapaApp(latitud, longitud)
    ventana.show()
    sys.exit(app.exec_())
