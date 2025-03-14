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
    QSizePolicy
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
        self.details_layout = QFormLayout()

        # Form Header
        self.form_header = QLabel("Detalles de la Orden")
        self.details_layout.addRow(self.form_header)
        self.details_layout.addRow(CQDivisor())

        # Order ID Input and Load Button
        self.order_id_input = QLineEdit()
        self.order_id_input.setPlaceholderText("Ingresar número de Orden")
        self.load_order_button = QPushButton("Cargar Orden")
        self.load_order_button.clicked.connect(self.load_order_details)
        self.details_layout.addRow(self.load_order_button, self.order_id_input)
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

        self.details_layout.addRow(CQDivisor())

        # Header seccion detalle de pagos
        self.payment_header_label = QLabel("Tabla: Registros de Pagos Por Orden")
        self.details_layout.addRow(self.payment_header_label)

        # Tabla detalle de pagos
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "No Orden", "Fecha Pagos", "Tipo de Pago", "Comentario", "Monto"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.details_layout.addRow(self.table)
        self.setLayout(self.details_layout)

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
            QMessageBox.warning(self, "Error", "Ingrese un número de orden válido")
            return
        else:
            # Fetch order details
            try:
                order = self.wo_service.get_work_order(order_id)
                # Fetch related data
                try:
                    client = self.client_service.get_client_by_id(order[5])
                    self.client_name_input.setText(client['name'])
                    self.client_phone_input.setText(client['contact_1'])
                    self.client_email_input.setText(client['email'])
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error fetching client details: {e}")
                try:
                    colaborator = self.colaborator_service.get_colaborator_by_id(order[6])
                    self.colaborator_name_input.setText(f"{colaborator[1]} {colaborator[2]}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error fetching colaborator details: {e}")
                try:
                    user = self.user_service.get_current_user()
                    self.user_name_input.setText(user.username)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error fetching user details: {e}")
                try:
                    order_balance = self.wo_service.work_order_balance(order[1])
                    if order_balance is not None:
                        if float(order_balance) < 0:
                            self.order_balance_input.setStyleSheet("color: red;")
                            self.order_balance_input.setText(str(order_balance))
                        else:
                            self.order_balance_input.setStyleSheet("color: green;")
                            self.order_balance_input.setText(str(order_balance))
                    else:
                        self.order_balance_input.setText("Balance no disponible") # o algun otro mensaje.
                    self.order_date_in_input.setText(order[2])
                    self.order_date_out_input.setText(order[3])
                    self.order_status_input.setText(order[8])
                    self.order_total_input.setText(str(order[7]))
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error fetching order balance: {e}")
                    return

                try:
                    paymet_details = self.wo_service.get_all_paymets_for_order(order[1])
                    self.table.setRowCount(len(paymet_details))
                    for row_index, payment in enumerate(paymet_details):
                        for col_index, value in enumerate(payment):
                            item = QTableWidgetItem(str(value))
                            self.table.setItem(row_index, col_index, item)
                    self.adjust_column_widths()

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error fetching all payments order: {e}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error fetching order details: {e}")
            return
