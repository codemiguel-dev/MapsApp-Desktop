import sys
import geopandas as gpd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MapaWidget(QWidget):
    def __init__(self, geojson_file, parent=None):
        super(MapaWidget, self).__init__(parent)
        self.geojson_file = geojson_file

        # Crear la figura de Matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.initUI()

    def initUI(self):
        # Layout vertical
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Cargar y mostrar el mapa
        self.cargar_mapa()

    def cargar_mapa(self):
        # Leer el archivo GeoJSON usando geopandas
        map_data = gpd.read_file(self.geojson_file)

        # Limpiar el eje y mostrar el mapa
        self.ax.clear()
        map_data.plot(ax=self.ax, color='lightblue', edgecolor='black')

        # Actualizar el canvas
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Configuración principal de la ventana
        self.setWindowTitle("Mapa de Natalidad")
        self.setGeometry(100, 100, 800, 600)

        # Ruta del archivo GeoJSON
        geojson_file = "natalidad.geojson"

        # Crear el widget de mapa y agregarlo a la ventana principal
        self.mapa_widget = MapaWidget(geojson_file, self)
        self.setCentralWidget(self.mapa_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())
