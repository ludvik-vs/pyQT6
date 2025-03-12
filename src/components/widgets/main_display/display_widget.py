from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Client
from src.components.forms.user.create_client import CreateClient
from src.components.forms.user.operaciones_client import ClientOperations
from src.components.tables.clients_table import ClientTableWidget

# Colaborator
from src.components.forms.user.create_colaborator import CreateColaborator
from src.components.tables.tabla_planilla import ColaboratorTableWidget
from src.components.forms.user.operaciones_colaborador import ColaboratorOperations
from src.components.forms.user.regitro_colaborador import ColaboratorRegister
from src.components.tables.user_table import UserTableWidget

# User
from src.components.forms.user.create_user import CreateUserForm
from src.components.forms.user.operaciones_user import UserOperations
from src.components.forms.user.change_password import PasswordChangeForm

# Orders
from src.components.forms.orders.create_orders import CrearOrdenForm

class DisplayWidget(QWidget):
    grid_layout: QGridLayout

    def __init__(self, auth_service, client_service, colaborator_service):
        super().__init__()
        self.setStyleSheet("background-color: #fafafc;")
        #--------------------------------------------------------------
        self.auth_service = auth_service
        self.auth_service.user_authenticated.connect(self.update_current_user_data)
        self.update_current_user_data(self.auth_service.get_current_user())
        self.current_user_data = None
        #--------------------------------------------------------------
        self.client_service = client_service
        #--------------------------------------------------------------
        self.colaborator_service = colaborator_service
        #--------------------------------------------------------------
        self.init_ui()

    def init_ui(self):
        self.grid_layout = QGridLayout()  # Usar grid_layout
        self.setLayout(self.grid_layout)

        # Asegúrate de que el layout se expanda
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setRowStretch(0, 1)

        # Mostrar la imagen inicial
        self.set_content("ACRIL CAR")

    def update_current_user_data(self, user):
        if user:
            self.current_user_data = user
        else:
            self.current_user_data = None
            print("No hay usuario autenticado")

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
            self.grid_layout.addWidget(image_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        elif text == "Cambiar Contraseña":
            form = PasswordChangeForm(self.current_user_data)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Alta de Cliente":
            form = CreateClient(self.client_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Operaciones con Cliente":
            form = ClientOperations(self.client_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Tabla de Clientes":
            form = ClientTableWidget(self.client_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Alta de Colaborador":
            form = CreateColaborator(self.colaborator_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Operaciones con Colaborador":
            form = ColaboratorOperations(self.colaborator_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Detalle por Colaborador":
            form = ColaboratorRegister(self.colaborator_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Tabla Planilla":
            form = ColaboratorTableWidget(self.colaborator_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Crear Orden":
            form = CrearOrdenForm(self.current_user_data, self.auth_service, self.client_service, self.colaborator_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Crear Usuario":
            form = CreateUserForm(self.auth_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Operaciones de Usuario":
            form = UserOperations(self.auth_service)
            self.grid_layout.addWidget(form, 0, 0)
        elif text == "Tabla Usuario":
            form = UserTableWidget(self.auth_service)
            self.grid_layout.addWidget(form, 0, 0)
        else:
            label = QLabel(f"Formulario para: {text}", self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(label, 0, 0)

    def clear_layout(self):
        """Elimina todos los widgets del layout."""
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
