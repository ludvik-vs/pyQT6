from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QSpinBox, QDoubleSpinBox, QMessageBox, QGroupBox,
    QScrollArea
)
from PyQt6.QtCore import Qt

class CashFlowControlForm(QWidget):
    def __init__(self, auth_service, cashbox_service):
        super().__init__()
        self.auth_service = auth_service
        self.cashbox_service = cashbox_service
        self.current_user = self.auth_service.get_current_user()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Header
        header = QLabel("Control de Caja")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(header)

        # Form Group
        form_group = QGroupBox("Información General")
        form_layout = QFormLayout()

        # Cash Count ID
        self.cash_count_id_input = QLineEdit()
        self.cash_count_id_input.setReadOnly(True)
        self.cash_count_id_input.setText(str(self.cashbox_service.get_last_cash_count_id_service() + 1))
        form_layout.addRow("No. de Arqueo:", self.cash_count_id_input)

        # Date and Time
        self.date_input = QLineEdit()
        self.date_input.setText(datetime.now().strftime("%d-%m-%Y"))
        form_layout.addRow("Fecha:", self.date_input)

        # Cashier
        self.cashier_input = QLineEdit(self.current_user.username)
        self.cashier_input.setReadOnly(True)
        form_layout.addRow("Cajero:", self.cashier_input)

        # Operation Type
        self.operation_type = QComboBox()
        self.operation_type.addItems(["apertura", "cierre"])
        form_layout.addRow("Tipo de Operación:", self.operation_type)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # Summary Group
        summary_group = QGroupBox("Resumen de Caja")
        summary_layout = QFormLayout()

        self.total_income = QLineEdit("0.00")
        self.total_income.setReadOnly(True)
        summary_layout.addRow("Total Ingresos:", self.total_income)

        self.total_expenses = QLineEdit("0.00")
        self.total_expenses.setReadOnly(True)
        summary_layout.addRow("Total Egresos:", self.total_expenses)

        self.expected_cash = QLineEdit("0.00")
        self.expected_cash.setReadOnly(True)
        summary_layout.addRow("Efectivo Esperado:", self.expected_cash)

        summary_group.setLayout(summary_layout)
        main_layout.addWidget(summary_group)

        # Cash Details Group
        cash_group = QGroupBox("Detalles de Efectivo")
        cash_layout = QFormLayout()

        # Initial/Final Cash
        self.cash_input = QDoubleSpinBox()
        self.cash_input.setRange(0, 1000000)
        self.cash_input.setDecimals(2)
        cash_layout.addRow("Monto en Caja:", self.cash_input)

        # Difference
        self.difference_input = QLineEdit("0.00")
        self.difference_input.setReadOnly(True)
        cash_layout.addRow("Diferencia:", self.difference_input)

        # Remarks
        self.remarks_input = QLineEdit()
        cash_layout.addRow("Observaciones:", self.remarks_input)

        cash_group.setLayout(cash_layout)
        main_layout.addWidget(cash_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.calculate_btn = QPushButton("Calcular Totales")
        self.calculate_btn.clicked.connect(self.calculate_totals)
        self.save_btn = QPushButton("Guardar")
        self.save_btn.clicked.connect(self.save_cash_count)
        button_layout.addWidget(self.calculate_btn)
        button_layout.addWidget(self.save_btn)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def calculate_totals(self):
        try:
            # Get the date from input
            fecha = self.date_input.text()

            # Get totals from service
            daily_totals = self.cashbox_service.get_daily_totals_service(fecha)

            total_income = daily_totals['total_ingresos']
            total_expenses = daily_totals['total_egresos']
            expected = total_income - total_expenses

            self.total_income.setText(f"{total_income:.2f}")
            self.total_expenses.setText(f"{total_expenses:.2f}")
            self.expected_cash.setText(f"{expected:.2f}")

            # Calculate difference
            actual_cash = self.cash_input.value()
            difference = actual_cash - expected
            self.difference_input.setText(f"{difference:.2f}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al calcular totales: {str(e)}")

    def save_cash_count(self):
        try:
            register_date = self.date_input.text()
            operation_type = self.operation_type.currentText()
            id_cajero = self.current_user.user_id
            initial_cash = self.cash_input.value()
            expected_cash = float(self.expected_cash.text())
            difference = float(self.difference_input.text())
            remarks = self.remarks_input.text()

            self.cashbox_service.create_cash_count_service(
                register_date=register_date,
                operation_type=operation_type,
                id_cajero=id_cajero,
                id_caja=1,
                initial_cash=initial_cash,
                final_cash=initial_cash,
                expected_cash=expected_cash,
                cash_difference=difference,
                remarks=remarks
            )

            # Update both cash count ID displays after saving
            new_id = self.cashbox_service.get_last_cash_count_id_service() + 1
            self.cash_count_id_input.setText(str(new_id))

            QMessageBox.information(self, "Éxito", "Registro guardado exitosamente")
            self.clear_form()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar registro: {str(e)}")

    def clear_form(self):
        """Clear all form inputs and reset to default values"""
        # Reset date to current
        self.date_input.setText(datetime.now().strftime("%d-%m-%Y"))

        # Reset operation type to first item
        self.operation_type.setCurrentIndex(0)

        # Clear summary values
        self.total_income.setText("0.00")
        self.total_expenses.setText("0.00")
        self.expected_cash.setText("0.00")

        # Reset cash input and difference
        self.cash_input.setValue(0.00)
        self.difference_input.setText("0.00")

        # Clear remarks
        self.remarks_input.clear()