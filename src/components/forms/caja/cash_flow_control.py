from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QSpinBox, QDoubleSpinBox, QMessageBox, QGroupBox,
    QScrollArea, QTableWidget, QTableWidgetItem,
    QSizePolicy, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer

class CashFlowControlForm(QWidget):
    def __init__(self, auth_service, cashbox_service):
        super().__init__()
        self.auth_service = auth_service
        self.cashbox_service = cashbox_service
        self.current_user = self.auth_service.get_current_user()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Header
        header = QLabel("Control de Flujo de Caja")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(header)

        # Date Group
        date_group = QGroupBox("Fecha de Consulta")
        date_layout = QFormLayout()
        self.date_input = QLineEdit()
        self.date_input.setText(datetime.now().strftime("%d-%m-%Y"))
        date_layout.addRow("Fecha:", self.date_input)
        date_group.setLayout(date_layout)
        main_layout.addWidget(date_group)

        # Summary Group
        summary_group = QGroupBox("Resumen General")
        summary_layout = QFormLayout()

        self.total_income = QLineEdit("0.00")
        self.total_income.setReadOnly(True)
        summary_layout.addRow("Total Ingresos:", self.total_income)

        self.total_expenses = QLineEdit("0.00")
        self.total_expenses.setReadOnly(True)
        summary_layout.addRow("Total Egresos:", self.total_expenses)

        self.net_cash = QLineEdit("0.00")
        self.net_cash.setReadOnly(True)
        summary_layout.addRow("Neto:", self.net_cash)

        summary_group.setLayout(summary_layout)
        main_layout.addWidget(summary_group)

        # Movements Summary Table
        movements_group = QGroupBox("Resumen por Movimientos")
        movements_layout = QVBoxLayout()
        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(3)
        self.movements_table.setHorizontalHeaderLabels(["Movimiento", "Tipo", "Monto"])
        self.movements_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.movements_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.movements_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Configure header for uniform distribution
        movements_header = self.movements_table.horizontalHeader()
        movements_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        movements_layout.addWidget(self.movements_table)
        movements_group.setLayout(movements_layout)
        main_layout.addWidget(movements_group)

        # Payment Methods Summary Table
        payments_group = QGroupBox("Resumen por Método de Pago")
        payments_layout = QVBoxLayout()
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(3)
        self.payments_table.setHorizontalHeaderLabels(["Método", "Tipo", "Monto"])
        self.payments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.payments_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.payments_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Configure header for uniform distribution
        payments_header = self.payments_table.horizontalHeader()
        payments_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        payments_layout.addWidget(self.payments_table)
        payments_group.setLayout(payments_layout)
        main_layout.addWidget(payments_group)

        # Expected Cash Group
        cash_group = QGroupBox("Efectivo en Caja")
        cash_layout = QFormLayout()
        self.expected_cash = QLineEdit("0.00")
        self.expected_cash.setReadOnly(True)
        cash_layout.addRow("Efectivo Esperado:", self.expected_cash)
        cash_group.setLayout(cash_layout)
        main_layout.addWidget(cash_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.calculate_btn = QPushButton("Calcular Totales")
        self.calculate_btn.clicked.connect(self.calculate_totals)
        button_layout.addWidget(self.calculate_btn)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        
        # Move the timer here, at the end of initUI
        QTimer.singleShot(100, self.adjust_tables)

    def calculate_totals(self):
        try:
            fecha = self.date_input.text()

            # Get general totals
            daily_totals = self.cashbox_service.get_daily_totals_service(fecha)
            total_income = daily_totals['total_ingresos']
            total_expenses = daily_totals['total_egresos']
            net_total = total_income - total_expenses

            self.total_income.setText(f"{total_income:.2f}")
            self.total_expenses.setText(f"{total_expenses:.2f}")
            self.net_cash.setText(f"{net_total:.2f}")

            # Get movement totals
            movement_totals = self.cashbox_service.get_movement_totals_service(fecha)
            self.movements_table.setRowCount(len(movement_totals))
            for i, (name, type_, amount) in enumerate(movement_totals):
                self.movements_table.setItem(i, 0, QTableWidgetItem(name))
                self.movements_table.setItem(i, 1, QTableWidgetItem(type_))
                self.movements_table.setItem(i, 2, QTableWidgetItem(f"{amount:.2f}"))

            # Get payment method totals
            payment_totals = self.cashbox_service.get_payment_method_totals_service(fecha)
            self.payments_table.setRowCount(len(payment_totals))
            expected_cash = 0
            for i, (method, type_, amount) in enumerate(payment_totals):
                self.payments_table.setItem(i, 0, QTableWidgetItem(method))
                self.payments_table.setItem(i, 1, QTableWidgetItem(type_))
                self.payments_table.setItem(i, 2, QTableWidgetItem(f"{amount:.2f}"))
                if method == 'efectivo':
                    if type_ == 'ingreso':
                        expected_cash += amount
                    else:
                        expected_cash -= amount

            self.expected_cash.setText(f"{expected_cash:.2f}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al calcular totales: {str(e)}")

    def clear_form(self):
        """Clear all form inputs and reset to default values"""
        self.date_input.setText(datetime.now().strftime("%d-%m-%Y"))
        self.total_income.setText("0.00")
        self.total_expenses.setText("0.00")
        self.net_cash.setText("0.00")
        self.expected_cash.setText("0.00")
        self.movements_table.setRowCount(0)
        self.payments_table.setRowCount(0)

    def adjust_tables(self):
        """Adjust column widths for both tables"""
        # Adjust movements table
        movements_width = self.movements_table.viewport().width()
        if movements_width > 0:
            column_width = int(movements_width / 3)
            for col in range(3):
                self.movements_table.setColumnWidth(col, column_width)

        # Adjust payments table
        payments_width = self.payments_table.viewport().width()
        if payments_width > 0:
            column_width = int(payments_width / 3)
            for col in range(3):
                self.payments_table.setColumnWidth(col, column_width)