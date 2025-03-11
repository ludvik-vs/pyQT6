from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal
from src.services.auth_service import AuthService
from src.services.auth_service import UserData  # Importa UserData

class LoginDialog(QDialog):
    login_successful = pyqtSignal(UserData)  # Cambia la señal para emitir UserData

    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.auth_service = auth_service
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setMinimumWidth(200)
        self.password_input = QLineEdit()
        self.password_input.setMinimumWidth(200)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Usuario:", self.username_input)
        form_layout.addRow("Contraseña:", self.password_input)

        login_button = QPushButton("Iniciar Sesión")
        login_button.clicked.connect(self.login)

        layout.addLayout(form_layout)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.auth_service.authenticate(username, password):
            user_data = self.auth_service.get_current_user()
            if user_data:
                self.login_successful.emit(user_data)  # Emite UserData directamente
                print("Login ok")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Error al obtener datos del usuario.")
                self.reject()
        else:
            print("Login Error")
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
            self.reject()

    def closeEvent(self, event):
        self.reject()
        event.accept()
