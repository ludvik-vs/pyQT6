from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from src.services.client_service import ClientService

class CreateClient(QWidget):
    def __init__(self, logs_service, auth_service, client_service: ClientService):
        super().__init__()
        self.logs_service = logs_service
        self.auth_service = auth_service
        self.client_service = client_service
        self.current_username_data = self.auth_service.get_current_user()
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

        # Nuevos campos
        self.numero_ruc_label = QLabel("Número RUC:")
        self.numero_ruc = QLineEdit(self)
        layout.addRow(self.numero_ruc_label, self.numero_ruc)

        self.nombre_empresa_label = QLabel("Nombre de la Empresa:")
        self.nombre_empresa = QLineEdit(self)
        layout.addRow(self.nombre_empresa_label, self.nombre_empresa)

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
        self.numero_ruc.clear()
        self.nombre_empresa.clear()
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
            numero_ruc = self.numero_ruc.text()
            nombre_empresa = self.nombre_empresa.text()
            
            if self.client_service.create_client(name, contact_1, contact_2, email, numero_ruc, nombre_empresa):
                self.clear_form()
                self.result_label.setStyleSheet("color: green;")
                self.result_label.setText("Cliente dado de alta exitosamente.")
                self.logs_service.register_activity(self.current_username_data.username,f"Alta de Cliente: {name}")
            else:
                self.clear_form()
                self.result_label.setStyleSheet("color: red;")
                self.result_label.setText("Error al dar de alta el cliente.")
        else:
            self.clear_form()
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Alta del cliente Cancelada.")
