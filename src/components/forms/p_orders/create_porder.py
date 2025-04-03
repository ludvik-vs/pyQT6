from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QLabel, QMessageBox,
    QVBoxLayout, QScrollArea, QTextEdit
)
from PyQt6.QtCore import Qt
import sqlite3

class CrearProductionOrdenForm(QWidget):
    def __init__(
        self,
        current_user_data,
        aunth_service,
        client_service,
        colaborator_service,
        work_order_service,
        production_order_service
    ):
        super().__init__()
        self.current_user_data = current_user_data
        self.aunth_service = aunth_service
        self.client_service = client_service
        self.colaborator_service = colaborator_service
        self.work_order_service = work_order_service
        self.production_order_service = production_order_service
        self.init_ui()

    def init_ui(self):
        # Establecer el fondo del formulario como transparente
        self.setStyleSheet("background-color: white;")

        # Create main layout
        main_layout = QVBoxLayout()

        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Create container widget for the form
        container = QWidget()

        # Añadir campos al layout
        self.details_layout = QFormLayout()
        self.details_layout.setVerticalSpacing(18)

        # Form Header
        self.fm_header = QLabel("Crear Orden de Producción", self)
        self.fm_header.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.details_layout.addRow(self.fm_header)

        # Campo para ingresar el número de orden
        self.orden_input = QLineEdit(self)
        self.orden_input.setPlaceholderText("Ingrese el número de orden")
        self.details_layout.addRow("Número de Orden:", self.orden_input)

        # Botón para cargar la orden
        self.cargar_orden_btn = QPushButton('Cargar Orden', self)
        self.cargar_orden_btn.clicked.connect(self.cargar_orden)
        self.details_layout.addRow(self.cargar_orden_btn)

        # Campos para mostrar los detalles de la orden
        self.start_date_label = QLabel("Fecha de Inicio:", self)
        self.details_layout.addRow(self.start_date_label)

        self.end_date_label = QLabel("Fecha de Fin:", self)
        self.details_layout.addRow(self.end_date_label)

        self.client_label = QLabel("Datos del Cliente:", self)
        self.details_layout.addRow(self.client_label)

        self.colaborador_label = QLabel("Asignado a:", self)
        self.details_layout.addRow(self.colaborador_label)

        # Change QLabel to QTextEdit for tasks details
        self.tasks_details_textArea = QTextEdit(self)
        self.tasks_details_textArea.setReadOnly(True)  # Make it read-only
        self.tasks_details_textArea.setMinimumHeight(100)  # Set minimum height
        self.tasks_details_textArea.setStyleSheet("background-color: #f0f0f0;")  # Light gray background
        self.details_layout.addRow("Detalles de Trabajo:", self.tasks_details_textArea)

        # Campo para agregar notas
        self.notes_textArea = QTextEdit(self)
        self.notes_textArea.setPlaceholderText("Agregar notas sobre la orden de producción...")
        self.notes_textArea.setMinimumHeight(100)  # Set minimum height
        self.details_layout.addRow("Notas:", self.notes_textArea)

        # Botón para crear la orden de producción
        self.crear_orden_btn = QPushButton('Procesar Orden', self)
        self.crear_orden_btn.clicked.connect(self.crear_orden_produccion)
        self.details_layout.addRow(self.crear_orden_btn)

        # Establecer el layout principal en el widget
        container.setLayout(self.details_layout)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def cargar_orden(self):
        """Cargar los datos de la orden de trabajo."""
        work_order_id = self.orden_input.text().strip()
        if not work_order_id:
            QMessageBox.critical(self, "Error", "Ingrese un número de orden válido.")
            return

        # Obtener datos de la orden de trabajo
        order_data = self.work_order_service.get_work_order(work_order_id)
        client_details = self.cargar_client_data(order_data[5])
        colaborador_details = self.cargar_colaborador_data(order_data[4])
        order_details_list = self.work_order_service.get_work_order_items(work_order_id)
        if order_data:
            self.start_date_label.setText(f"Fecha de Inicio: {order_data[2]}")
            self.end_date_label.setText(f"Fecha de Fin: {order_data[3]}")
            self.client_label.setText(f"Cliente: {client_details}")
            self.colaborador_label.setText(f"Colaborador: {colaborador_details}")

            # Format tasks details with line breaks
            tasks_text = ""
            if order_details_list:
                for item in order_details_list:
                    services_str = item[3]  # Assuming the services are in the 4th column
                    services_list = eval(services_str)

                    for service in services_list:
                        tasks_text += f"• {service}\n"

                self.tasks_details_textArea.setText(tasks_text)
            else:
                self.tasks_details_textArea.setText("No hay tareas registradas")
        else:
            QMessageBox.warning(self, "Advertencia", "Orden de trabajo no encontrada.")

    def cargar_client_data(self, client_id):
        client_data = self.client_service.get_client_by_id(client_id)
        return f"{client_data['name']} | {client_data['contact_1']}"

    def cargar_colaborador_data(self, colaborador_id):
        colaborador_data = self.colaborator_service.get_colaborator_by_id(colaborador_id)
        return f"{colaborador_data[1]} {colaborador_data[2]}"

    def crear_orden_produccion(self):
        """Crear una nueva orden de producción con los datos cargados."""
        work_order_id = self.orden_input.text().strip()
        if not work_order_id:
            QMessageBox.critical(self, "Error", "Ingrese un número de orden válido.")
            return

        # Obtener datos de la orden de trabajo
        order_data = self.work_order_service.get_work_order(work_order_id)
        order_task_details = self.tasks_details_textArea.toPlainText()
        note = self.notes_textArea.toPlainText()

        if order_data:
            try:
                # Crear la orden de producción con estado "procesando"
                self.production_order_service.create_production_order(
                    work_order_id=work_order_id,
                    start_date=order_data[2],
                    end_date=order_data[3],
                    colaborador_id=order_data[4],
                    client_id=order_data[5],
                    product_id=None,
                    quantity=None,
                    order_status="procesando",
                    tasks_details=order_task_details,
                    note=note
                )
                QMessageBox.information(self, "Éxito", "Orden de producción creada exitosamente.")
                self.clean_form()
                self.work_order_service.update_work_order(work_order_id, order_status="procesando")
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    QMessageBox.warning(self, "Advertencia", "Esta orden de trabajo ya tiene una orden de producción creada.")
                else:
                    QMessageBox.critical(self, "Error", "Error de integridad en la base de datos.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear la orden de producción: {str(e)}")
        else:
            QMessageBox.warning(self, "Advertencia", "Orden de trabajo no encontrada.")

    def clean_form(self):
        """Limpiar el formulario."""
        self.orden_input.clear()
        self.start_date_label.setText("Fecha de Inicio:")
        self.end_date_label.setText("Fecha de Fin:")
        self.client_label.setText("Cliente:")
        self.colaborador_label.setText("Colaborador:")
        self.tasks_details_textArea.clear()
        self.notes_textArea.clear()  # Clear the note text area
        self.orden_input.setFocus()

    def closeEvent(self, event):
        """Evento que se ejecuta cuando se cierra la ventana."""
        self.clean_form()
        event.accept()  # Accept the close event to close the window

