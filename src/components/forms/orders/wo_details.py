from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QTextEdit
)
from src.components.custom.cq_divisor import CQDivisor

class WorkOrderDetails(QWidget):
    """
    Interfaz que muestra todos los detalles de una orden de trabajo.
    Args:
        parent (QWidget): Parent widget.
        wo_service (WorkOrderService): Service for work order operations.
        client_service (ClientService): Service for client operations.
        colaborator_service (ColaboratorService): Service for colaborator operations.
        user_service (AuthService): Service for user operations.
    Returns:
        None
    Raises:
        ValueError: If parent is not a valid QWidget.
        AttributeError: If any service is not provided.
        TypeError: If any service is not an instance of its respective class.
    """
    def __init__(self, wo_service, client_service, colaborator_service, user_service):
        super().__init__()
        self.wo_service = wo_service
        self.client_service = client_service
        self.colaborator_service = colaborator_service
        self.user_service = user_service
        self.init_ui()

    def init_ui(self):
        # Implement UI setup here
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Create container widget for the form
        container = QWidget()
        self.details_layout = QFormLayout()

        # Form Header
        self.form_header = QLabel("Detalles de la Orden")
        self.form_header.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.details_layout.addRow(self.form_header)
        self.details_layout.addRow(CQDivisor())

        self.h_order_layout = QHBoxLayout()
        # Order ID Input and Load Button
        self.order_id_input = QLineEdit()
        self.order_id_input.setPlaceholderText("Ingresar número de Orden")
        self.load_order_button = QPushButton("Cargar Orden")
        self.load_order_button.clicked.connect(self.load_order_details)
        self.h_order_layout.addWidget(self.order_id_input)
        self.h_order_layout.addWidget(self.load_order_button)
        self.details_layout.addRow(self.h_order_layout)
        self.details_layout.addRow(CQDivisor())

        self.client_name_label = QLabel("Nombre del Cliente:")
        self.client_name_input = QLineEdit()
        self.client_name_input.setReadOnly(True)
        self.details_layout.addRow(self.client_name_label, self.client_name_input)

        self.client_phone_label = QLabel("Teléfono del Cliente:")
        self.client_phone_input = QLineEdit()
        self.client_phone_input.setReadOnly(True)
        self.details_layout.addRow(self.client_phone_label, self.client_phone_input)

        self.client_email_label = QLabel("Email del Cliente:")
        self.client_email_input = QLineEdit()
        self.client_email_input.setReadOnly(True)
        self.details_layout.addRow(self.client_email_label, self.client_email_input)
        self.details_layout.addRow(CQDivisor())

        #---------------------------------------------
        self.colaborator_name_label = QLabel("Asignado a:")
        self.colaborator_name_input = QLineEdit()
        self.colaborator_name_input.setReadOnly(True)
        self.details_layout.addRow(self.colaborator_name_label, self.colaborator_name_input)

        self.user_name_label = QLabel("Registrado por:")
        self.user_name_input = QLineEdit()
        self.user_name_input.setReadOnly(True)
        self.details_layout.addRow(self.user_name_label, self.user_name_input)
        self.details_layout.addRow(CQDivisor())

        # Order details
        self.order_date_in_label = QLabel("Fecha de Ingreso:")
        self.order_date_in_input = QLineEdit()
        self.order_date_in_input.setReadOnly(True)
        self.details_layout.addRow(self.order_date_in_label, self.order_date_in_input)

        self.order_date_out_label = QLabel("Fecha de Entrega:")
        self.order_date_out_input = QLineEdit()
        self.order_date_out_input.setReadOnly(True)
        self.details_layout.addRow(self.order_date_out_label, self.order_date_out_input)

        self.order_status_label = QLabel("Estado de Orden:")
        self.order_status_input = QLineEdit()
        self.order_status_input.setReadOnly(True)
        self.details_layout.addRow(self.order_status_label, self.order_status_input)

        self.order_total_label = QLabel("Precio Total de la Orden (C$):")
        self.order_total_input = QLineEdit()
        self.order_total_input.setReadOnly(True)
        self.details_layout.addRow(self.order_total_label, self.order_total_input)

        self.order_balance_label = QLabel("Balance de Orden (C$):")
        self.order_balance_input = QLineEdit()
        self.order_balance_input.setReadOnly(True)
        self.details_layout.addRow(self.order_balance_label, self.order_balance_input)

        self.order_note_label = QLabel("Notas de la Orden: ")
        self.order_note_text = QTextEdit()
        self.details_layout.addRow(self.order_note_label, self.order_note_text)

        self.details_layout.addRow(CQDivisor())

        # Header seccion detalle de pagos
        self.payment_header_label = QLabel("Tabla: Registros de Pagos Por Orden")
        self.details_layout.addRow(self.payment_header_label)

        # Tabla detalle de pagos
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        # work_order_id, payment_date, payment_method, payment, user_log_registration, note
        self.table.setHorizontalHeaderLabels([
            "ID", "No Orden", "Fecha Pagos", "Tipo de Pago", "Registrado por", "Monto (C$)", "Comentario", 
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.details_layout.addRow(self.table)

        # Close order red Btn
        self.close_order_button = QPushButton("Cerrar Orden")
        # disable Btn
        self.close_order_button.setVisible(False)
        self.close_order_button.clicked.connect(self.close_order)

        # Add container to scroll area
        container.setLayout(self.details_layout)
        # Set container as the scroll area widget
        scroll.setWidget(container)
        # Add scroll area to the main layout
        main_layout.addWidget(scroll)
        # Add close order button to the main layout
        main_layout.addWidget(self.close_order_button)
        # Add the main layout to the widget
        self.setLayout(main_layout)

    def adjust_column_widths(self):
        table_width = self.table.viewport().width()
        column_count = self.table.columnCount()
        if column_count > 0 and table_width > 0:
            equal_width = int(table_width / column_count)
            for col_index in range(column_count):
                self.table.setColumnWidth(col_index, equal_width)
        else:
            default_column_width = 20
            for col_index in range(column_count):
                self.table.setColumnWidth(col_index, default_column_width)

    def load_order_details(self):
        order_id = self.order_id_input.text()
        if not order_id:
            self.show_error("warning", "Ingrese un número de orden válido")
            return

        try:
            order = self.wo_service.get_work_order(order_id)
            self.load_client_details(order[5])
            self.load_colaborator_details(order[6])
            self.load_user_details()
            self.load_order_balance(order[1])
            self.load_order_info(order)
            self.load_payment_details(order[1])
            self.load_order_status(order[8])
            

        except Exception as e:
            self.show_error("Error", f"Error al buscar la orden, verifique el numero de orden ingresado:  <<{e}>>")
            return

    def load_client_details(self, client_id):
        try:
            client = self.client_service.get_client_by_id(client_id)
            self.client_name_input.setText(client['name'])
            self.client_phone_input.setText(client['contact_1'])
            self.client_email_input.setText(client['email'])
        except Exception as e:
            self.show_error("Error", f"Error en la busqueda de los detalles del client: {e}")

    def load_colaborator_details(self, colaborator_id):
        try:
            colaborator = self.colaborator_service.get_colaborator_by_id(colaborator_id)
            self.colaborator_name_input.setText(f"{colaborator[1]} {colaborator[2]}")
        except Exception as e:
            self.show_error("Error", f"Error en la busqueda de los datos del colaborator: {e}")

    def load_user_details(self):
        try:
            user = self.user_service.get_current_user()
            self.user_name_input.setText(user.username)
        except Exception as e:
            self.show_error("Error", f"Error en la busqueda de los datos de usuario: {e}")

    def load_order_balance(self, order_id):
        try:
            order_balance = self.wo_service.work_order_balance(order_id)
            
            if order_balance is not None:
                if float(order_balance) == 0:
                    self.order_balance_input.setStyleSheet("color: green;")
                    self.close_order_button.setStyleSheet("color: green;")
                    self.close_order_button.setVisible(True)
                else:
                    self.close_order_button.setVisible(False)
                    self.order_balance_input.setStyleSheet("color: orange;")
                    
                self.order_balance_input.setText(str(order_balance))
            else:
                self.order_balance_input.setText("Balance no disponible")
        except Exception as e:
            self.show_error("Error", f"Error error en la busqueda del balance de la orden: {e}")

    def load_order_info(self, order):
        self.order_date_in_input.setText(order[2])
        self.order_date_out_input.setText(order[3])
        self.order_status_input.setText(order[8])
        self.order_total_input.setText(str(order[7]))
        self.order_note_text.setText(order[9])

    def load_payment_details(self, order_id):
        try:
            paymet_details = self.wo_service.get_all_paymets_for_order(order_id)
            self.table.setRowCount(len(paymet_details))
            for row_index, payment in enumerate(paymet_details):
                for col_index, value in enumerate(payment):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row_index, col_index, item)
            self.adjust_column_widths()
        except Exception as e:
            self.show_error("Error", f"Error en la busqueda de los detalles de pago de la orden: {e}")

    def load_order_status(self, order_status):
        if order_status == "Abierta":
            self.order_status_input.setStyleSheet("color: red;")
        else:
            self.close_order_button.setVisible(False)
            self.order_status_input.setStyleSheet("color: green;")

    def close_order(self):
        order_id = self.order_id_input.text()
        if not order_id:
            self.show_error("warning", "Ingrese un número de orden válido")
            return

        # Confirmation dialog
        confirmation = QMessageBox()
        confirmation.setIcon(QMessageBox.Icon.Warning)
        confirmation.setWindowTitle("Confirmar Cierre de Orden")
        confirmation.setText("¿Está seguro de cerrar esta orden?")
        confirmation.setInformativeText("Una vez cerrada la orden, no podrá ser reabierta.\nPor favor, verifique que todos los detalles estén correctos.")
        confirmation.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirmation.setDefaultButton(QMessageBox.StandardButton.No)

        if confirmation.exec() == QMessageBox.StandardButton.Yes:
            try:
                self.wo_service.update_work_order(order_id, order_status='Cerrada')
                self.load_order_details()
                self.show_error("info", "Orden cerrada correctamente")
            except Exception as e:
                self.show_error("error", f"Error al cerrar la orden: {e}")

    def show_error(self, message_type="error", message=""):
        if message_type.lower() == "error":
            QMessageBox.critical(self, "Error", message)
        elif message_type.lower() == "warning":
            QMessageBox.warning(self, "Advertencia", message)
        elif message_type.lower() == "info":
            QMessageBox.information(self, "Información", message)
