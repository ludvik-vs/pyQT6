from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
#from src.db.database_manager import DatabaseManager
from src.db.db_operations.db_client import DatabaseClient
from src.components.forms.orders.create_orders import CrearOrdenForm
from src.components.forms.user.create_client import CreateClient
from src.services.client_service import ClientService
from src.components.forms.user.operaciones_client import ClientOperations
from src.components.tables.clients_table import ClientTableWidget

class DisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fafafc;")
        self.db_manager = DatabaseClient()
        self.client_service = ClientService(self.db_manager)
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Set the column stretch factor for the first (and only) column to 80%
        self.layout.setColumnStretch(0,0)

        # Mostrar la imagen inicial
        self.set_content("ACRIL CAR")

    def set_content(self, text):
        """Actualiza el contenido del widget según el sub-elemento seleccionado."""
        # Limpiar el layout antes de agregar nuevos widgets
        self.clear_layout()

        if text == "ACRIL CAR":
            # Crear un nuevo QLabel para mostrar la imagen
            image_label = QLabel(self)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setScaledContents(True)
            image_label.setFixedSize(800, 600)

            # Cargar la imagen
            pixmap = QPixmap('assets/acril_car_banner.jpg')
            image_label.setPixmap(pixmap)
            self.layout.addWidget(image_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        elif text == "Alta de Cliente":
            form = CreateClient(self.client_service)
            self.layout.addWidget(form, 0, 0, Qt.AlignmentFlag.AlignCenter)
        elif text == "Operaciones con Cliente":
            form = ClientOperations(self.client_service)
            self.layout.addWidget(form, 0, 0, Qt.AlignmentFlag.AlignCenter)
        elif text == "Tabla de Clientes":
            form = ClientTableWidget(self.client_service)
            self.layout.addWidget(form)
        elif text == "Crear Orden":
            form = CrearOrdenForm()
            self.layout.addWidget(form, 0, 0, Qt.AlignmentFlag.AlignCenter)
        else:
            label = QLabel(f"Formulario para: {text}", self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    def clear_layout(self):
        """Elimina todos los widgets del layout."""
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()