import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QStyleFactory, QWidget, QGridLayout, QDialog
from PyQt6.QtGui import QScreen

# USER
from src.db.db_operations.db_user import DatabaseUser
from src.services.auth_service import AuthService

# COLABORATOR
from src.db.db_operations.db_colaborator import DatabaseColaborators
from src.services.rh_service import ColaboratorService

# CLIENT
from src.db.db_operations.db_client import DatabaseClient
from src.services.client_service import ClientService

# COMPONENTS
from src.components.widgets.aside_bar.aside_widget import AsideWidget
from src.components.widgets.main_display.display_widget import DisplayWidget
from src.components.login.login_dialog import LoginDialog

# WORK ORDERS
from src.db.db_operations.db_work_order import DatabaseWorkOrder
from src.services.work_order_service import WorkOrderService

# CASHBOX
from src.db.db_operations.db_cashbox import DBCashBox
from src.services.cashbox_service import CashBoxService

# PRODUCTION ORDER
from src.db.db_operations.db_productions_orders import DatabaseProductionOrders
from src.services.production_order_service import ProductionOrderService

# LOGS
from src.db.db_operations.db_logs import DBLogs
from src.services.logs_services import LogsServices

def load_styles():
    if getattr(sys, 'frozen', False):
        # Entorno empaquetado: usar sys._MEIPASS para acceder al directorio temporal
        base_path = sys._MEIPASS
        file_path = os.path.join(base_path, 'src', 'styles', 'main.css')
    else:
        # Entorno de desarrollo: usar la ruta relativa desde el script
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'src', 'styles', 'main.css')
    
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Warning: Style file not found at {file_path}")
        return ""  # Return empty string if file not found

# Add these imports at the top with other imports
from src.api.server import APIServer
from src.config.api import APIConfig

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ACRIL CAR NI")
        self.setStyleSheet(load_styles())
        
        # Initialize API Server
        self.api_server = APIServer()
        
        #--------------------------------------------------------------
        self.db_logs = DBLogs()
        self.logs_service = LogsServices(self.db_logs)
        #--------------------------------------------------------------
        self.user_db_manager = DatabaseUser()
        self.user_db_manager.connect(self.user_db_manager.db_name)
        self.auth_service = AuthService(self.user_db_manager)
        #--------------------------------------------------------------
        self.db_client = DatabaseClient()
        self.client_service = ClientService(self.db_client)
        #--------------------------------------------------------------
        self.db_colaborator = DatabaseColaborators()
        self.colaborator_service = ColaboratorService(self.db_colaborator)
        #--------------------------------------------------------------
        self.db_work_order = DatabaseWorkOrder()
        self.work_order_service = WorkOrderService(self.db_work_order)
        #--------------------------------------------------------------
        self.db_productio_order = DatabaseProductionOrders()
        self.work_productio_service = ProductionOrderService(self.db_productio_order)
        #--------------------------------------------------------------
        self.db_cashbox = DBCashBox()
        self.cashbox_service = CashBoxService(self.db_cashbox)
        #--------------------------------------------------------------
        self.aside_widget = AsideWidget(self.logs_service, self.auth_service)
        self.display_widget = DisplayWidget(
            self.logs_service,
            self.auth_service, 
            self.client_service, 
            self.colaborator_service, 
            self.work_order_service,
            self.cashbox_service,
            self.work_productio_service
        )
        self.login_form = LoginDialog(self.auth_service)
        self.init_ui()
        self.aside_widget.tree_menu.item_selected.connect(self.update_display)
        self.login_form.login_successful.connect(self.on_login_success)
        self.setStyle(QApplication.style())
        self.aside_widget.setStyle(QApplication.style())
        self.display_widget.setStyle(QApplication.style())
        self.login_form.setStyle(QApplication.style())

    def update_display(self, text):
        """Actualiza el contenido del DisplayWidget con el texto del ítem seleccionado."""
        self.display_widget.set_content(text)

    def start_login(self):
        """Iniciar el diálogo de login y manejar el resultado."""
        print("Iniciando diálogo de login...")
        self.center_login_form()
        result = self.login_form.exec()
        print(f"Resultado del diálogo: {result}")

        if result == QDialog.DialogCode.Accepted:
            self.show()
        else:
            self.handle_login_failure()

    def handle_login_failure(self):
        """Manejar el fallo del login."""
        print("Cerrando base de datos...")
        self.user_db_manager.close()
        print("Saliendo del programa...")
        sys.exit(0)

    def on_login_success(self, user_data):
        """Manejar el éxito del login."""
        print("Login exitoso")
        self.logs_service.register_activity(user_data.username, "Inicio de sesión")

    def center_login_form(self):
        """Centrar el diálogo de login en la pantalla."""
        screen_geometry = QScreen.availableGeometry(QApplication.primaryScreen())
        login_form_geometry = self.login_form.frameGeometry()
        login_form_geometry.moveCenter(screen_geometry.center())
        self.login_form.move(login_form_geometry.topLeft())

    def init_ui(self):
        """Configurar la interfaz principal."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(central_widget)
        grid_layout.setHorizontalSpacing(0)
        grid_layout.setVerticalSpacing(0)
        grid_layout.addWidget(self.aside_widget, 0, 0)
        grid_layout.addWidget(self.display_widget, 0, 1)
        grid_layout.setColumnStretch(0, 20)
        grid_layout.setColumnStretch(1, 80)
        central_widget.setLayout(grid_layout)

if __name__ == "__main__":
    print("Iniciando aplicación...")
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = MainWindow()
    
    # Start API server if enabled
    if APIConfig.SERVER_ENABLED:
        window.api_server.start()
    
    # Register cleanup function for application exit
    def cleanup():
        if hasattr(window.auth_service, 'current_user') and window.auth_service.current_user:
            window.logs_service.register_activity(
                window.auth_service.current_user.username, 
                "Cierre de Sesión"
            )
        # Stop API server if it was started
        if APIConfig.SERVER_ENABLED:
            window.api_server.stop()
    
    app.aboutToQuit.connect(cleanup)
    
    window.start_login()
    print("Entrando al bucle de eventos...")
    sys.exit(app.exec())
