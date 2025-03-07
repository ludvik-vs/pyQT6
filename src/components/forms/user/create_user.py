from PyQt6.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from src.services.auth_service import AuthService

class CreateUserForm(QWidget):
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #f4f4f4;")
        layout = QFormLayout()  # Usar QFormLayout
        layout.setVerticalSpacing(10)

        self.username_label = QLabel('Nombre de usuario:')
        self.username_input = QLineEdit()
        layout.addRow(self.username_label, self.username_input)

        self.password_label = QLabel('Contraseña:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(self.password_label, self.password_input)

        self.role_label = QLabel('Rol:')
        self.role_combobox = QComboBox()
        self.role_combobox.addItems(['user', 'admin'])
        layout.addRow(self.role_label, self.role_combobox)

        self.create_button = QPushButton('Crear Usuario')
        layout.addRow(self.create_button)  # Agregar el botón directamente al layout

        # Conectar el botón a la función create_user
        self.create_button.clicked.connect(self.create_user)

        self.setLayout(layout)
        self.setWindowTitle('Crear Usuario')

    def create_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combobox.currentText()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Por favor, complete todos los campos.')
            return

        success = self.auth_service.register_user(username, password, role)
        if success:
            QMessageBox.information(self, 'Éxito', 'Usuario creado exitosamente.')
            self.clear_form()  # Limpiar el formulario después de crear el usuario
        else:
            QMessageBox.warning(self, 'Error', 'No se pudo crear el usuario.')

    def clear_form(self):
        """Limpiar todos los campos del formulario."""
        self.username_input.clear()
        self.password_input.clear()
        self.role_combobox.setCurrentIndex(0)  # Restablecer el rol a 'user'
