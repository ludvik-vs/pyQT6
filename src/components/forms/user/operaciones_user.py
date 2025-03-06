from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem, QCheckBox, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt
from src.services.auth_service import AuthService

class UserOperatiosn(QWidget):
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f4f4f4;")

        # Campos del formulario
        self.user_id_input = QLineEdit(self)
        self.username_input = QLineEdit(self)
        self.username_input.setReadOnly(True)
        self.role_input = QLineEdit(self)
        self.role_input.setReadOnly(True)

        # Botones
        self.load_button = QPushButton('Cargar Datos del Usuario', self)
        self.save_button = QPushButton('Guardar Accesos', self)
        self.clear_button = QPushButton('Limpiar Formulario', self)
        self.delete_button = QPushButton('Eliminar Usuario', self)

        # Conectar botones a sus funciones
        self.load_button.clicked.connect(self.load_user_data)
        self.save_button.clicked.connect(self.save_user_access)
        self.clear_button.clicked.connect(self.clear_form)
        self.delete_button.clicked.connect(self.delete_user)

        # Layout principal
        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
        form_layout.setVerticalSpacing(18)

        # Añadir campos al layout
        form_layout.addRow(QLabel("ID del Usuario:", self), self.user_id_input)
        form_layout.addRow(self.load_button)
        form_layout.addRow(QLabel("Nombre de Usuario:", self), self.username_input)
        form_layout.addRow(QLabel("Rol:", self), self.role_input)

        # Crear checkboxes para accesos
        self.access_checkboxes = self.create_access_checkboxes()
        access_groupbox = QGroupBox("Accesos", self)
        access_layout = QVBoxLayout()
        for checkbox in self.access_checkboxes:
            access_layout.addWidget(checkbox)
        access_groupbox.setLayout(access_layout)

        # Añadir accesos al layout principal
        form_layout.addRow(access_groupbox)

        # Añadir botones a un contenedor horizontal
        button_container = QHBoxLayout()
        button_container.addWidget(self.clear_button)
        button_container.addWidget(self.save_button)
        button_container.addWidget(self.delete_button)

        # Crear el layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer)
        main_layout.addLayout(button_container)

        # Establecer el layout principal en el widget
        self.setLayout(main_layout)

        # Label para resultados
        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.result_label)

        # Asegurarse de que el formulario ocupe todo el ancho del contenedor padre
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def create_access_checkboxes(self):
        """Crear checkboxes para los accesos."""
        access_list = [
            'Inicio', 'Clientes', 'Planilla', 'Operaciones con Ordenes',
            'Operaciones de Caja', 'Reportes Operativos', 'Reportes Administrativos',
            'Administración de Usuarios', 'Operaciones de Administración'
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
        self.result_label.clear()
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
