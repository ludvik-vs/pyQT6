from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton
from src.services.auth_service import AuthService
from src.db.db_operations.db_user import DatabaseUser

class PasswordChangeForm(QWidget):

    def __init__(self, logs_service, current_user_data):
        super().__init__()
        self.logs_service = logs_service
        self.current_user_data = current_user_data
        self.db_user = DatabaseUser()
        self.auth_serive = AuthService(self.db_user)
        self.init_ui()

    def init_ui(self):
        """Inicializar la interfaz de usuario."""
        self.setStyleSheet("background-color: #f4f4f4;")
        layout = QFormLayout()
        layout.setVerticalSpacing(18)

        # Campos del formulario
        self.current_id_label = QLabel("ID Usuario:")
        self.current_id = QLabel(str(self.current_user_data.user_id))
        layout.addRow(self.current_id_label, self.current_id)

        self.current_user_label = QLabel("Usuario Actual: ")
        self.current_user = QLabel(self.current_user_data.username)
        layout.addRow(self.current_user_label, self.current_user)

        self.current_password_label = QLabel("Contraseña Actual:")
        self.current_password = QLineEdit(self)
        self.current_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(self.current_password_label, self.current_password)

        self.new_password_label = QLabel("Nueva Contraseña:")
        self.new_password = QLineEdit(self)
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(self.new_password_label, self.new_password)

        self.confirm_password_label = QLabel("Confirmar Contraseña:")
        self.confirm_password = QLineEdit(self)
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(self.confirm_password_label, self.confirm_password)

        # Botones
        button_container = QHBoxLayout()
        button_container.setSpacing(60)

        self.limpiar_btn = QPushButton('Limpiar Formulario', self)
        self.limpiar_btn.clicked.connect(self.clear_form)
        button_container.addWidget(self.limpiar_btn)

        self.cambiar_password_btn = QPushButton('Cambiar Contraseña', self)
        self.cambiar_password_btn.clicked.connect(self.cambiar_password)
        button_container.addWidget(self.cambiar_password_btn)

        layout.addRow(button_container)

        self.result_label = QLabel(self)
        layout.addRow(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle('Cambiar Contraseña')

    def clear_form(self):
        """Limpiar todos los campos del formulario."""
        self.current_password.clear()
        self.new_password.clear()
        self.confirm_password.clear()
        self.result_label.clear()

    def cambiar_password(self):
        """Cambiar la contraseña del usuario."""
        current_password = self.current_password.text()
        new_password = self.new_password.text()
        confirm_password = self.confirm_password.text()

        if not current_password or not new_password or not confirm_password:
            self.result_label.setText("Por favor, complete todos los campos.")
            return

        if new_password != confirm_password:
            self.result_label.setText("Las contraseñas no coinciden.")
            return

        if not self.auth_serive.verify_password(self.current_user_data.user_id, current_password):
            self.result_label.setText("La contraseña actual es incorrecta.")
            return

        self.auth_serive.change_password(self.current_user_data.user_id, new_password)
        self.clear_form()
        self.result_label.setText("Contraseña cambiada exitosamente.")
        self.logs_service.register_activity(self.current_user_data.username, "Cambio de contraseña")
        QApplication.instance().quit()
