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
from src.components.tables.wo_table import WorkOrderTable
from src.components.forms.orders.wo_details import WorkOrderDetails
from src.components.forms.orders.cancel_order import CancelOrderForm

# Caja
from src.components.forms.caja.ingresos import FormularioIngresoCaja
from src.components.forms.caja.cash_movements import CashMovementForm
from src.components.forms.caja.salidas import FormularioEgresoCaja
from src.components.forms.caja.cash_balance import CashBalanceForm
from src.components.forms.caja.cash_flow_control import CashFlowControlForm

class DisplayWidget(QWidget):
    grid_layout: QGridLayout

    def __init__(
        self, 
        auth_service, 
        client_service, 
        colaborator_service, 
        work_order_service, 
        cashbox_service
    ):
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
        self.work_order_service = work_order_service
        #--------------------------------------------------------------
        self.cashbox_service = cashbox_service
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
        self.clear_layout()

        widget_map = {
            "ACRIL CAR": self.show_acril_car_image,
            "Cambiar Contraseña": lambda: self.grid_layout.addWidget(
                PasswordChangeForm(self.current_user_data), 0, 0),
            "Alta de Cliente": lambda: self.grid_layout.addWidget(
                CreateClient(self.client_service), 0, 0),
            "Operaciones con Cliente": lambda: self.grid_layout.addWidget(
                ClientOperations(self.client_service), 0, 0),
            "Tabla de Clientes": lambda: self.grid_layout.addWidget(
                ClientTableWidget(self.client_service), 0, 0),
            "Alta de Colaborador": lambda: self.grid_layout.addWidget(
                CreateColaborator(self.colaborator_service), 0, 0),
            "Operaciones con Colaborador": lambda: self.grid_layout.addWidget(
                ColaboratorOperations(self.colaborator_service), 0, 0),
            "Detalle por Colaborador": lambda: self.grid_layout.addWidget(
                ColaboratorRegister(self.colaborator_service), 0, 0),
            "Tabla Planilla": lambda: self.grid_layout.addWidget(
                ColaboratorTableWidget(self.colaborator_service), 0, 0),
            "Crear Orden T": lambda: self.grid_layout.addWidget(
                CrearOrdenForm(
                    self.current_user_data,
                    self.auth_service,
                    self.client_service,
                    self.colaborator_service,
                    self.work_order_service), 0, 0),
            "Detalle Orden T": lambda: self.grid_layout.addWidget(WorkOrderDetails(
                self.work_order_service,
                self.client_service,
                self.colaborator_service,
                self.auth_service), 0, 0),
            "Tabla Orden T": lambda: self.grid_layout.addWidget(
                WorkOrderTable(self.work_order_service), 0, 0),
            "Ingresos de Caja": lambda: self.grid_layout.addWidget(
                FormularioIngresoCaja(
                    self.auth_service,
                    self.client_service,
                    self.work_order_service,
                    self.cashbox_service
                ), 0, 0),
            "Egresos de Caja": lambda: self.grid_layout.addWidget(
                FormularioEgresoCaja(
                    self.auth_service,
                    self.work_order_service,
                    self.cashbox_service
            ), 0, 0),
            "Arqueo de Efectivo en Caja": lambda: self.grid_layout.addWidget(
                CashBalanceForm(
                    self.auth_service,
                    self.cashbox_service
            ), 0, 0),
            "Crear Usuario": lambda: self.grid_layout.addWidget(CreateUserForm(
                self.auth_service), 0, 0),
            "Operaciones de Usuario": lambda: self.grid_layout.addWidget(UserOperations(
                self.auth_service), 0, 0),
            "Tabla Usuario": lambda: self.grid_layout.addWidget(UserTableWidget(
                self.auth_service), 0, 0),
            "Anular Orden": lambda: self.grid_layout.addWidget(
                CancelOrderForm(
                    self.current_user_data,
                    self.auth_service,
                    self.work_order_service,
                ), 0, 0),
            "Balance Entradas|Salidas": lambda: self.grid_layout.addWidget(
                CashFlowControlForm(
                    self.auth_service,
                    self.cashbox_service,
                ), 0, 0),
            "Catalogo de Movimientos": lambda: self.grid_layout.addWidget(
                CashMovementForm(
                    self.cashbox_service,
                    self.auth_service
                ), 0, 0),
        }

        action = widget_map.get(text)
        if action:
            action()
        else:
            label = QLabel(f"Formulario para: {text}", self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(label, 0, 0)

    def show_acril_car_image(self):
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setScaledContents(True)
        image_label.setFixedSize(800, 600)
        pixmap = QPixmap('assets/acril_car_banner.jpg')
        image_label.setPixmap(pixmap)
        self.grid_layout.addWidget(image_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    def clear_layout(self):
        """Elimina todos los widgets del layout."""
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
