from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
from src.services.client_service import ClientService

class ClientOperations(QWidget):
    def __init__(self, client_service: ClientService):
        super().__init__()
        self.client_service = client_service
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f4f4f4;")

        # Campos del formulario
        self.client_id = QLineEdit(self)
        self.nombre_cliente = QLineEdit(self)
        self.nombre_cliente.setMinimumWidth(600)
        self.phone_contacto_1 = QLineEdit(self)
        self.phone_contacto_2 = QLineEdit(self)
        self.email = QLineEdit(self)

        # Botones
        self.load_btn = QPushButton('Cargar datos del Cliente', self)
        self.limpiar_btn = QPushButton('Limpiar Formulario', self)
        self.actualizar_cliente_btn = QPushButton('Actualizar Cliente', self)
        self.eliminar_cliente_btn = QPushButton('Eliminar Cliente', self)

        # Conectar botones a sus funciones
        self.load_btn.clicked.connect(self.load_client)
        self.limpiar_btn.clicked.connect(self.clear_form)
        self.actualizar_cliente_btn.clicked.connect(self.actualizar_cliente)
        self.eliminar_cliente_btn.clicked.connect(self.eliminar_cliente)

        # Layout principal
        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
        form_layout.setVerticalSpacing(18)

        # Otros campos
        client_id_label = QLabel("ID del Cliente:", self)
        client_id_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(client_id_label, self.client_id)
        form_layout.addRow(self.load_btn)
        nombre_label = QLabel("Nombre Completo del Cliente:", self)
        nombre_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(nombre_label, self.nombre_cliente)

        phone_1_label = QLabel("Teléfono Contacto 1:", self)
        phone_1_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(phone_1_label, self.phone_contacto_1)

        phone2_label = QLabel("Teléfono Contacto 2:", self)
        phone2_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(phone2_label, self.phone_contacto_2)

        correo_label = QLabel("Correo Electrónico:", self)
        correo_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(correo_label, self.email)

        # Añadir botones a un contenedor horizontal
        button_container = QHBoxLayout()
        button_container.addWidget(self.limpiar_btn)
        button_container.addWidget(self.actualizar_cliente_btn)
        button_container.addWidget(self.eliminar_cliente_btn)

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

    def load_client(self):
        """Cargar datos del cliente desde la base de datos usando el ID."""
        client_id = self.client_id.text().strip()
        if not client_id:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Por favor ingrese un ID de cliente.")
            return

        # Nota: Esto asume que tienes un método get_client_by_id en ClientService
        client_data = self.client_service.get_client_by_id(client_id)

        if client_data:
            self.nombre_cliente.setText(client_data["name"])
            self.phone_contacto_1.setText(client_data["contact_1"])
            self.phone_contacto_2.setText(client_data["contact_2"])
            self.email.setText(client_data["email"])
            self.result_label.setStyleSheet("color: green;")
            self.result_label.setText("Cliente cargado exitosamente.")
        else:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Cliente no encontrado.")

    def clear_form(self):
        """Limpiar todos los campos del formulario."""
        self.client_id.clear()
        self.nombre_cliente.clear()
        self.phone_contacto_1.clear()
        self.phone_contacto_2.clear()
        self.email.clear()
        self.result_label.clear()

    def actualizar_cliente(self):
        client_id_text = self.client_id.text().strip()
        name = self.nombre_cliente.text()
        contact_1 = self.phone_contacto_1.text()
        contact_2 = self.phone_contacto_2.text()
        email = self.email.text()

        if not client_id_text:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Por favor cargue un cliente primero.")
            return

        try:
            client_id = int(client_id_text)  # Convertir el ID de string a integer
        except ValueError:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("El ID del cliente debe ser un número válido.")
            return

        confirmation = QMessageBox.question(
            self,
            "Confirmar Actualización",
            "¿Está seguro de que desea actualizar este cliente?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            # Usar client_id en lugar de email como identificador
            if self.client_service.update_client_by_id(client_id, name, contact_1, contact_2, email):
                self.result_label.setStyleSheet("color: green;")
                self.result_label.setText("Cliente actualizado exitosamente.")
                self.clear_form()
            else:
                self.result_label.setStyleSheet("color: red;")
                self.result_label.setText("Error al actualizar el cliente.")
                self.clear_form()
        else:
            self.clear_form()
            self.result_label.setStyleSheet("color: orange;")
            self.result_label.setText("Actualización de cliente cancelada.")

    def eliminar_cliente(self):
        client_id_text = self.client_id.text().strip()

        if not client_id_text:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Por favor ingrese un ID de cliente.")
            return

        try:
            client_id = int(client_id_text)  # Convertir el ID de string a integer
        except ValueError:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("El ID del cliente debe ser un número válido.")
            return

        # Obtener datos del cliente usando el ID
        client_data = self.client_service.get_client_by_id(client_id)

        if client_data:
            confirmation = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                "¿Está seguro de que desea eliminar este cliente?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirmation == QMessageBox.StandardButton.Yes:
                if self.client_service.remove_client(client_id):
                    self.result_label.setStyleSheet("color: green;")
                    self.result_label.setText("Cliente eliminado exitosamente.")
                    self.clear_form()  # Limpiar formulario después de eliminar
                else:
                    self.result_label.setStyleSheet("color: red;")
                    self.result_label.setText("Error al eliminar el cliente.")
                    self.clear_form()
            else:
                self.result_label.setStyleSheet("color: orange;")
                self.result_label.setText("Eliminación cancelada.")
                self.clear_form()
        else:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Cliente no encontrado.")
            self.clear_form()
