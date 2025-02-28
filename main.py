import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QDialog
from PyQt6.QtGui import QScreen
from src.services.auth_service import AuthService
from src.db.database_manager import DatabaseManager
from src.components.widgets.aside_bar.aside_widget import AsideWidget
from src.components.widgets.main_display.display_widget import DisplayWidget
from src.components.login.login_dialog import LoginDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setStyleSheet("background-color: #04011c")
        self.setStyleSheet("background-color: lightgrey")
        self.db_manager = DatabaseManager()
        self.db_manager.connect()
        self.auth_service = AuthService(self.db_manager)
        self.aside_widget = AsideWidget(self.auth_service)
        self.display_widget = DisplayWidget()
        self.login_form = LoginDialog(self.auth_service)
        self.showMaximized()

        # Conectar signal del TreeMenu con el slot de MainWindow
        self.aside_widget.tree_menu.item_selected.connect(self.update_display)
    
    def update_display(self, text):
        """Actualiza el contenido del DisplayWidget con el texto del ítem seleccionado."""
        self.display_widget.set_content(text)

    def start_login(self):
        """Iniciar el diálogo de login y manejar el resultado."""
        print("Iniciando diálogo de login...")
        self.login_form.login_successful.connect(self.on_login_success)
        result = self.login_form.exec()
        print(f"Resultado del diálogo: {result}")

        if result == QDialog.DialogCode.Rejected:
            print("Cerrando base de datos...")
            self.db_manager.close()
            print("Saliendo del programa...")
            sys.exit(0)
        else:
            print("Login exitoso, continuando...")

    def on_login_success(self, user_data):
        """Manejar el éxito del login."""
        print(f"Login exitoso: {user_data}")
        self.init_ui()
        self.login_form.accept()
        self.showMaximized()
        self.maximize_to_screen()

    def maximize_to_screen(self):
        """Ajustar la ventana al tamaño de la pantalla."""
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.resize(screen.size())
        self.move(screen.topLeft())

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
    window = MainWindow()
    window.start_login()
    print("Entrando al bucle de eventos...")
    sys.exit(app.exec())