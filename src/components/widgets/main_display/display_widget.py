from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Client
from src.db.db_operations.db_client import DatabaseClient
from src.services.client_service import ClientService
from src.components.forms.user.create_client import CreateClient
from src.components.forms.user.operaciones_client import ClientOperations
from src.components.tables.clients_table import ClientTableWidget

# Colaborator
from src.services.rh_service import ColaboratorService
from src.components.forms.user.create_colaborator import CreateColaborator
from src.components.tables.tabla_planilla import ColaboratorTableWidget
from src.components.forms.user.operaciones_colaborador import ColaboratorOperations
from src.components.forms.user.regitro_colaborador import ColaboratorRegister
from src.components.tables.user_table import UserTableWidget

# User
from src.db.db_operations.db_user import DatabaseUser
from src.services.auth_service import AuthService
from src.components.forms.user.create_user import CreateUserForm
from src.components.forms.user.operaciones_user import UserOperatiosn

# Orders
from src.components.forms.orders.create_orders import CrearOrdenForm

class DisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fafafc;")
        #--------------------------------------------------------------
        self.client_db_manager = DatabaseClient()
        self.client_service = ClientService(self.client_db_manager)
        #--------------------------------------------------------------
        self.colaborator_service = ColaboratorService()
        #--------------------------------------------------------------
        self.user_db_manager = DatabaseUser()
        self.user_services = AuthService(self.user_db_manager)
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Asegúrate de que el layout se expanda
        self.layout.setColumnStretch(0, 1)
        self.layout.setRowStretch(0, 1)

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
            self.layout.addWidget(form, 0, 0)
        elif text == "Operaciones con Cliente":
            form = ClientOperations(self.client_service)
            self.layout.addWidget(form, 0, 0)
        elif text == "Tabla de Clientes":
            form = ClientTableWidget(self.client_service)
            self.layout.addWidget(form, 0, 0)
        elif text == "Alta de Colaborador":
            form = CreateColaborator(self.colaborator_service)
            self.layout.addWidget(form, 0, 0)
        elif text == "Operaciones con Colaborador":
            form = ColaboratorOperations(self.colaborator_service)
            self.layout.addWidget(form, 0, 0)
        elif text == "Detalle por Colaborador":
            form = ColaboratorRegister()
            self.layout.addWidget(form, 0, 0)
        elif text == "Tabla Planilla":
            form = ColaboratorTableWidget(self.colaborator_service)
            self.layout.addWidget(form, 0, 0)
        elif text == "Crear Orden":
            form = CrearOrdenForm()
            self.layout.addWidget(form, 0, 0)
        elif text == "Crear Usuario":
            form = CreateUserForm(self.user_services)
            self.layout.addWidget(form, 0, 0)
        elif text == "Operaciones de Usuario":
            form = UserOperatiosn(self.user_services)
            self.layout.addWidget(form, 0, 0)
        elif text == "Tabla Usuario":
            form = UserTableWidget(self.user_services)
            self.layout.addWidget(form, 0, 0)
        else:
            label = QLabel(f"Formulario para: {text}", self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(label, 0, 0)

    def clear_layout(self):
        """Elimina todos los widgets del layout."""
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
