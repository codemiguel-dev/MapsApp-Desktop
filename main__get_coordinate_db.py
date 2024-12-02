import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWebChannel import QWebChannel

class CoordinateHandler(QObject):
    coordinatesReceived = pyqtSignal(list)  # Signal para emitir las coordenadas a JavaScript

    @pyqtSlot(str, float, float)
    def updateCoordinates(self, updatedCoordinates, lat, lon):
        updatedCoordinates = json.loads(updatedCoordinates)
        file_path = 'coordenada.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Filtrar las coordenadas eliminando la que coincide con lat y lon
        existing_data = [coord for coord in existing_data if not (coord['latitude'] == lat and coord['longitude'] == lon)]

        # Guardar los datos actualizados
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

        print(f"Coordenada eliminada: Latitud: {lat}, Longitud: {lon}")

class MapsAppGet(QMainWindow):
    def __init__(self):
        super(MapsAppGet, self).__init__()
        self.webView = QWebEngineView(self)
        self.setCentralWidget(self.webView)
        self.resize(800, 600)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mapa_html = os.path.join(current_dir, "mapa_get_coordinate.html")
        url_base = QUrl.fromLocalFile(mapa_html)
        self.webView.setUrl(url_base)

        self.channel = QWebChannel()
        self.coordinate_handler = CoordinateHandler()
        self.channel.registerObject("pyqtObj", self.coordinate_handler)
        self.webView.page().setWebChannel(self.channel)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MapsAppGet()
    ventana.show()
    sys.exit(app.exec_())
