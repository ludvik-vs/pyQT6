from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal

class CQServicesList(QWidget):
    # Define una señal que emite una lista de tareas en formato de texto
    services_updated = pyqtSignal(str)

    def __init__(self, service_list_data: list[None]):
        super().__init__()
        self.services = service_list_data if service_list_data is not None else []
        self.init_ui()

    def init_ui(self):
        # Asegúrate de que self.v_layout es una instancia de QVBoxLayout
        self.v_layout = QVBoxLayout()

        # Frame horizontal para el input y el botón
        self.input_frame = QHBoxLayout()
        self.input_frame.setSpacing(10)

        # Input para nuevo servicio
        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("Ingresar descripción de servicio")
        self.input_frame.addWidget(self.service_input)

        # Botón para agregar servicio
        self.add_button = QPushButton("Agregar Servicio")
        self.add_button.clicked.connect(self.add_service)
        self.input_frame.addWidget(self.add_button)

        # Agrega el frame horizontal al layout vertical
        self.v_layout.addLayout(self.input_frame)

        # Lista para mostrar servicios
        self.service_list_widget = QListWidget()
        self.v_layout.addWidget(self.service_list_widget)

        # Inicializa la lista de servicios
        self.update_service_list()

        self.setLayout(self.v_layout)

    def clear(self):
        """Limpiar la lista de servicios y el campo de entrada."""
        self.services.clear()
        self.service_input.clear()
        self.update_service_list()

    def add_service(self):
        service_text = self.service_input.text().strip()
        if service_text:
            self.services.append(service_text)
            self.service_input.clear()
            self.update_service_list()
            # Emitir la señal con la lista actualizada de tareas
            self.services_updated.emit(str(self.services))

    def update_service_list(self):
        self.service_list_widget.clear()
        for index, service in enumerate(self.services, start=1):
            item_text = f"{index}. {service}"
            item = QListWidgetItem(item_text)
            self.service_list_widget.addItem(item)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def get_services(self):
        return self.services
