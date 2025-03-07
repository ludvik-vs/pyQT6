from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from src.services.client_service import ClientService

class CreateClient(QWidget):
    def __init__(self, client_service: ClientService):
        super().__init__()
        self.client_service = client_service
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f4f4f4;")
        layout = QFormLayout()
        layout.setVerticalSpacing(18)

        # Campos del formulario
        self.nombre_cliente_label = QLabel("Nombre Completo del Cliente:")
        self.nombre_cliente = QLineEdit(self)
        layout.addRow(self.nombre_cliente_label, self.nombre_cliente)

        self.phone_contacto_1_label = QLabel("Teléfono Contacto 1:")
        self.phone_contacto_1 = QLineEdit(self)
        layout.addRow(self.phone_contacto_1_label, self.phone_contacto_1)

        self.phone_contacto_2_label = QLabel("Teléfono Contacto 2:")
        self.phone_contacto_2 = QLineEdit(self)
        layout.addRow(self.phone_contacto_2_label, self.phone_contacto_2)

        self.email_label = QLabel("Correo Electrónico:")
        self.email = QLineEdit(self)
        layout.addRow(self.email_label, self.email)

        # Botones
        button_container = QHBoxLayout()
        button_container.setSpacing(60)

        self.limpiar_btn = QPushButton('Limpiar Formulario', self)
        self.limpiar_btn.clicked.connect(self.clear_form)
        button_container.addWidget(self.limpiar_btn)

        self.alta_cliente_btn = QPushButton('Alta de Cliente', self)
        self.alta_cliente_btn.clicked.connect(self.alta_cliente)
        button_container.addWidget(self.alta_cliente_btn)
        layout.addRow(button_container)

        self.result_label = QLabel(self)
        layout.addRow(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle('Alta de Cliente')

    def clear_form(self):
        """Limpiar todos los campos del formulario."""
        self.nombre_cliente.clear()
        self.phone_contacto_1.clear()
        self.phone_contacto_2.clear()
        self.email.clear()
        self.result_label.clear()

    def alta_cliente(self):
        """Dar de alta un cliente y mostrar un diálogo de confirmación."""
        confirmation = QMessageBox.question(
            self,
            "Confirmar Alta",
            "¿Está seguro de que desea dar de alta este cliente?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            name = self.nombre_cliente.text()
            contact_1 = self.phone_contacto_1.text()
            contact_2 = self.phone_contacto_2.text()
            email = self.email.text()

            if self.client_service.create_client(name, contact_1, contact_2, email):
                self.clear_form()
                self.result_label.setStyleSheet("color: green;")
                self.result_label.setText("Cliente dado de alta exitosamente.")
            else:
                self.clear_form()
                self.result_label.setStyleSheet("color: red;")
                self.result_label.setText("Error al dar de alta el cliente.")
        else:
            self.clear_form()
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Alta del cliente Cancelada.")
