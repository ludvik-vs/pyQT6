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
        # Establecer el fondo del formulario como gris claro
        self.setStyleSheet("background-color: #f4f4f4;")

        # Campos del formulario
        self.nombre_cliente = QLineEdit(self)
        self.nombre_cliente.setMinimumWidth(600)
        self.phone_contacto_1 = QLineEdit(self)
        self.phone_contacto_2 = QLineEdit(self)
        self.email = QLineEdit(self)

        # Botones
        self.limpiar_btn = QPushButton('Limpiar Formulario', self)
        self.alta_cliente_btn = QPushButton('Alta de Cliente', self)

        # Conectar botones a sus respectivas funciones
        self.limpiar_btn.clicked.connect(self.clear_form)
        self.alta_cliente_btn.clicked.connect(self.alta_cliente)

        # Añadir campos al layout
        layout = QFormLayout()
        layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
        layout.setVerticalSpacing(18)

        # Crear QLabels con fondo transparente
        nombre_label = QLabel("Nombre Completo del Cliente:", self)
        layout.addRow(nombre_label, self.nombre_cliente)

        phone_1_label = QLabel("Teléfono Contacto 1:", self)
        layout.addRow(phone_1_label, self.phone_contacto_1)

        phone2_label = QLabel("Teléfono Contacto 2:", self)
        layout.addRow(phone2_label, self.phone_contacto_2)

        correo_label = QLabel("Correo Electrónico:", self)
        layout.addRow(correo_label, self.email)


        # Crear un layout horizontal para los botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(60)
        button_layout.addWidget(self.limpiar_btn)
        button_layout.addWidget(self.alta_cliente_btn)

        # Añadir el layout de botones al layout principal
        layout.addRow(button_layout)

        self.setLayout(layout)

        # Label para mostrar el resultado de la operación
        self.result_label = QLabel(self)
        self.result_label.setStyleSheet("background-color: transparent;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        # Asegurarse de que el formulario ocupe todo el ancho del contenedor padre
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

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
