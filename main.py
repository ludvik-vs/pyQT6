import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QStyleFactory, QWidget, QGridLayout, QDialog
from PyQt6.QtGui import QScreen
from src.services.auth_service import AuthService
from src.db.db_operations.db_user import DatabaseUser
from src.components.widgets.aside_bar.aside_widget import AsideWidget
from src.components.widgets.main_display.display_widget import DisplayWidget
from src.components.login.login_dialog import LoginDialog

def load_styles():
    with open("main.css", "r") as file:
        return file.read()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ACRIL CAR NI")
        self.setStyleSheet(load_styles())
        self.user_db_manager = DatabaseUser()
        self.user_db_manager.connect()
        self.auth_service = AuthService(self.user_db_manager)
        self.aside_widget = AsideWidget(self.auth_service)
        self.display_widget = DisplayWidget()
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
    window.start_login()
    print("Entrando al bucle de eventos...")
    sys.exit(app.exec())
