from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox, QGroupBox, QMessageBox
)
from src.services.auth_service import AuthService

class UserOperations(QWidget):
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f4f4f4;")
        layout = QFormLayout()
        layout.setVerticalSpacing(10)

        # Campos del formulario
        self.user_id_label = QLabel("ID del Usuario:")
        self.user_id_input = QLineEdit(self)
        layout.addRow(self.user_id_label, self.user_id_input)

        self.load_button = QPushButton('Cargar Datos', self)
        layout.addRow(self.load_button)

        self.username_label = QLabel("Nombre de Usuario:")
        self.username_input = QLineEdit(self)
        self.username_input.setReadOnly(True)
        layout.addRow(self.username_label, self.username_input)

        self.role_label = QLabel("Rol:")
        self.role_input = QLineEdit(self)
        self.role_input.setReadOnly(True)
        layout.addRow(self.role_label, self.role_input)

        self.save_button = QPushButton('Guardar Accesos', self)
        self.clear_button = QPushButton('Limpiar Formulario', self)
        self.delete_button = QPushButton('Eliminar Usuario', self)

        # Conectar botones a sus funciones
        self.load_button.clicked.connect(self.load_user_data)
        self.save_button.clicked.connect(self.save_user_access)
        self.clear_button.clicked.connect(self.clear_form)
        self.delete_button.clicked.connect(self.delete_user)

        # Crear checkboxes para accesos
        self.access_checkboxes = self.create_access_checkboxes()
        access_groupbox = QGroupBox("Accesos", self)
        access_layout = QVBoxLayout()
        for checkbox in self.access_checkboxes:
            access_layout.addWidget(checkbox)
        access_groupbox.setLayout(access_layout)
        layout.addRow(access_groupbox)

        # Añadir botones a un contenedor horizontal
        button_container = QHBoxLayout()
        button_container.addWidget(self.clear_button)
        button_container.addWidget(self.save_button)
        button_container.addWidget(self.delete_button)
        button_container.setSpacing(18)
        layout.addRow(button_container)

        self.setLayout(layout)
        self.setWindowTitle('Operaciones Con Usuarios')

    def create_access_checkboxes(self):
        """Crear checkboxes para los accesos."""
        access_list = [
            '1 - Inicio',
            '2 - Administración de Usuarios',
            '3 - Clientes',
            '4 - Órdenes de Trabajo',
            '5 - Órdenes de Producción',
            '6 - Operaciones de Caja',
            '7 - Reportes Operativos',
            '8 - Planilla',
            '9 - Operaciones de Administración',
            '10 - Reportes Administrativos'
        ]
        checkboxes = []
        for access in access_list:
            checkbox = QCheckBox(access, self)
            checkboxes.append(checkbox)
        return checkboxes

    def load_user_data(self):
        """Cargar datos del usuario y sus accesos."""
        user_id = self.user_id_input.text().strip()
        if not user_id:
            self.show_message("Por favor ingrese un ID de usuario.", QMessageBox.Icon.Critical)
            return

        try:
            user_id = int(user_id)  # Convertir el ID de string a integer
        except ValueError:
            self.show_message("El ID del usuario debe ser un número válido.", QMessageBox.Icon.Critical)
            return

        # Obtener todos los usuarios y buscar por ID
        all_users = self.auth_service.db_manager.get_all_users()
        user_data = next((user for user in all_users if user["id"] == user_id), None)

        if user_data:
            self.username_input.setText(user_data["username"])
            self.role_input.setText(user_data["role"])
            self.load_user_access(user_id)
            self.show_message("Datos del usuario cargados exitosamente.", QMessageBox.Icon.Information)
        else:
            self.show_message("Usuario no encontrado.", QMessageBox.Icon.Warning)

    def load_user_access(self, user_id):
        """Cargar los accesos del usuario y marcar los checkboxes correspondientes."""
        accesses = self.auth_service.db_manager.get_user_access(user_id)
        access_dict = {access[0]: access[1] for access in accesses}

        for checkbox in self.access_checkboxes:
            branch_name = checkbox.text()
            checkbox.setChecked(branch_name in access_dict)

    def save_user_access(self):
        """Guardar los accesos seleccionados para el usuario."""
        user_id = self.user_id_input.text().strip()
        if not user_id:
            self.show_message("Por favor ingrese un ID de usuario.", QMessageBox.Icon.Critical)
            return

        try:
            user_id = int(user_id)  # Convertir el ID de string a integer
        except ValueError:
            self.show_message("El ID del usuario debe ser un número válido.", QMessageBox.Icon.Critical)
            return

        # Obtener accesos seleccionados
        selected_accesses = [checkbox.text() for checkbox in self.access_checkboxes if checkbox.isChecked()]

        # Revocar todos los accesos actuales
        current_accesses = self.auth_service.db_manager.get_user_access(user_id)
        for access in current_accesses:
            self.auth_service.db_manager.revoke_access(user_id, access[0], access[1])

        # Otorgar los nuevos accesos seleccionados
        for access in selected_accesses:
            self.auth_service.db_manager.grant_access(user_id, access)

        self.show_message("Accesos guardados exitosamente.", QMessageBox.Icon.Information)
        self.clear_form()

    def clear_form(self):
        """Limpiar todos los campos del formulario."""
        self.user_id_input.clear()
        self.username_input.clear()
        self.role_input.clear()
        for checkbox in self.access_checkboxes:
            checkbox.setChecked(False)

    def show_message(self, message, icon):
        """Mostrar un mensaje emergente con el texto y el ícono especificados."""
        msg_box = QMessageBox(self)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()

    def delete_user(self):
        """Eliminar el usuario y sus accesos."""
        user_id = self.user_id_input.text().strip()
        if not user_id:
            self.show_message("Por favor ingrese un ID de usuario.", QMessageBox.Icon.Critical)
            return

        try:
            user_id = int(user_id)  # Convertir el ID de string a integer
        except ValueError:
            self.show_message("El ID del usuario debe ser un número válido.", QMessageBox.Icon.Critical)
            return

        # Confirmar la eliminación
        confirmation = QMessageBox.question(
            self, "Confirmar Eliminación",
            "¿Está seguro de que desea eliminar este usuario y todos sus accesos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            # Eliminar accesos del usuario
            accesses = self.auth_service.db_manager.get_user_access(user_id)
            for access in accesses:
                self.auth_service.db_manager.revoke_access(user_id, access[0], access[1])

            # Eliminar el usuario
            if self.auth_service.db_manager.remove_user(user_id):
                self.show_message("Usuario y accesos eliminados exitosamente.", QMessageBox.Icon.Information)
                self.clear_form()
            else:
                self.show_message("No se pudo eliminar el usuario.", QMessageBox.Icon.Warning)
