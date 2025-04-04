from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout
)
from src.services.client_service import ClientService

class ClientOperations(QWidget):
    def __init__(self, client_service: ClientService):
        super().__init__()
        self.client_service = client_service
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f4f4f4;")
        layout = QFormLayout()
        layout.setVerticalSpacing(18)

        # Campos del formulario
        self.client_id_label = QLabel("ID del Cliente:")
        self.client_id = QLineEdit(self)
        layout.addRow(self.client_id_label, self.client_id)

        self.load_btn = QPushButton('Cargar Cliente', self)
        layout.addRow(self.load_btn)

        self.nombre_cliente_label = QLabel("Nombre del Cliente:")
        self.nombre_cliente = QLineEdit(self)
        layout.addRow(self.nombre_cliente_label, self.nombre_cliente)

        self.phone_contact_1_label = QLabel("Teléfono de Contacto 1:")
        self.phone_contacto_1 = QLineEdit(self)
        layout.addRow(self.phone_contact_1_label, self.phone_contacto_1)

        self.phone_contact_2_label = QLabel("Teléfono de Contacto 2:")
        self.phone_contacto_2 = QLineEdit(self)
        layout.addRow(self.phone_contact_2_label, self.phone_contacto_2)

        self.email_label = QLabel("Correo Electrónico:")
        self.email = QLineEdit(self)
        layout.addRow(self.email_label, self.email)

        # Nuevos campos
        self.numero_ruc_label = QLabel("Número RUC:")
        self.numero_ruc = QLineEdit(self)
        layout.addRow(self.numero_ruc_label, self.numero_ruc)

        self.nombre_empresa_label = QLabel("Nombre de la Empresa:")
        self.nombre_empresa = QLineEdit(self)
        layout.addRow(self.nombre_empresa_label, self.nombre_empresa)

        # Botones
        self.limpiar_btn = QPushButton('Limpiar Formulario', self)
        self.actualizar_cliente_btn = QPushButton('Actualizar Cliente', self)
        self.eliminar_cliente_btn = QPushButton('Eliminar Cliente', self)

        # Conectar botones a sus funciones
        self.load_btn.clicked.connect(self.load_client)
        self.limpiar_btn.clicked.connect(self.clear_form)
        self.actualizar_cliente_btn.clicked.connect(self.actualizar_cliente)
        self.eliminar_cliente_btn.clicked.connect(self.eliminar_cliente)

        # Añadir botones a un contenedor horizontal
        button_container = QHBoxLayout()
        button_container.addWidget(self.limpiar_btn)
        button_container.addWidget(self.actualizar_cliente_btn)
        button_container.addWidget(self.eliminar_cliente_btn)
        button_container.setSpacing(18)
        layout.addRow(button_container)

        # Label para resultados
        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def load_client(self):
        """Cargar datos del cliente desde la base de datos usando el ID."""
        client_id = self.client_id.text().strip()
        if not client_id:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Por favor ingrese un ID de cliente.")
            return

        client_data = self.client_service.get_client_by_id(client_id)

        if client_data:
            self.nombre_cliente.setText(client_data["name"])
            self.phone_contacto_1.setText(client_data["contact_1"])
            self.phone_contacto_2.setText(client_data["contact_2"])
            self.email.setText(client_data["email"])
            self.numero_ruc.setText(client_data["numero_ruc"])
            self.nombre_empresa.setText(client_data["nombre_empresa"])
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
        self.numero_ruc.clear()
        self.nombre_empresa.clear()
        self.result_label.clear()

    def actualizar_cliente(self):
        client_id_text = self.client_id.text().strip()
        name = self.nombre_cliente.text()
        contact_1 = self.phone_contacto_1.text()
        contact_2 = self.phone_contacto_2.text()
        email = self.email.text()
        numero_ruc = self.numero_ruc.text()
        nombre_empresa = self.nombre_empresa.text()

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
            if self.client_service.update_client_by_id(client_id, name, contact_1, contact_2, email, numero_ruc, nombre_empresa):
                self.clear_form()
                self.result_label.setStyleSheet("color: green;")
                self.result_label.setText("Cliente actualizado exitosamente.")
            else:
                self.clear_form()
                self.result_label.setStyleSheet("color: red;")
                self.result_label.setText("Error al actualizar el cliente.")
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
                    self.clear_form()
                    self.result_label.setStyleSheet("color: green;")
                    self.result_label.setText("Cliente eliminado exitosamente.")
                else:
                    self.clear_form()
                    self.result_label.setStyleSheet("color: red;")
                    self.result_label.setText("Error al eliminar el cliente.")
            else:
                self.clear_form()
                self.result_label.setStyleSheet("color: orange;")
                self.result_label.setText("Eliminación cancelada.")
        else:
            self.clear_form()
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Cliente no encontrado.")
