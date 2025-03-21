from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QSpinBox, QDoubleSpinBox, QMessageBox, QGroupBox,
    QTabWidget, QScrollArea
)
from PyQt6.QtCore import Qt

class CashBalanceForm(QWidget):

    def __init__(self, auth_service, cashbox_service):
        super().__init__()
        self.auth_service = auth_service
        self.cashbox_service = cashbox_service
        self.current_user = self.auth_service.get_current_user()
        self.denominations = [
            ('1000', 1000), ('500', 500), ('200', 200), 
            ('100', 100), ('50', 50), ('20', 20), 
            ('10', 10), ('5', 5), ('1', 1), 
            ('0.5', 0.5), ('0.25', 0.25), ('0.1', 0.1),
            ('0.05', 0.05), ('0.01', 0.01)
        ]
        self.denomination_inputs = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Create tabs
        tabs = QTabWidget()
        tabs.addTab(self.createCashRegisterTab(), "Apertura/Cierre")
        tabs.addTab(self.createDenominationsTab(), "Arqueo de Efectivo")
        layout.addWidget(tabs)
        
        self.setLayout(layout)

    def createCashRegisterTab(self):
        widget = QWidget()
        layout = QFormLayout()

        # Header
        header = QLabel("Control de Caja")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addRow(header)

        # Cash Count ID
        self.cash_count_id_input = QLineEdit()
        self.cash_count_id_input.setReadOnly(True)
        self.cash_count_id_input.setText(str(self.cashbox_service.get_last_cash_count_id_service() + 1))
        layout.addRow("No. de Arqueo:", self.cash_count_id_input)

        # Date and Time - Make it editable
        self.date_input = QLineEdit()
        self.date_input.setText(datetime.now().strftime("%d-%m-%Y"))
        layout.addRow("Fecha:", self.date_input)

        # Cashier
        self.cashier_input = QLineEdit(self.current_user.username)
        self.cashier_input.setReadOnly(True)
        layout.addRow("Cajero:", self.cashier_input)

        # Operation Type
        self.operation_type = QComboBox()
        self.operation_type.addItems(["apertura", "cierre"])
        layout.addRow("Tipo de Operación:", self.operation_type)

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
        layout.addRow(summary_group)

        # Initial/Final Cash
        self.cash_input = QDoubleSpinBox()
        self.cash_input.setRange(0, 1000000)
        self.cash_input.setDecimals(2)
        layout.addRow("Monto en Caja:", self.cash_input)

        # Difference
        self.difference_input = QLineEdit("0.00")
        self.difference_input.setReadOnly(True)
        layout.addRow("Diferencia:", self.difference_input)

        # Remarks
        self.remarks_input = QLineEdit()
        layout.addRow("Observaciones:", self.remarks_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar")
        self.save_btn.clicked.connect(self.save_cash_count)
        self.calculate_btn = QPushButton("Calcular Totales")
        self.calculate_btn.clicked.connect(self.calculate_totals)
        button_layout.addWidget(self.calculate_btn)
        button_layout.addWidget(self.save_btn)
        layout.addRow(button_layout)

        widget.setLayout(layout)
        return widget

    def createDenominationsTab(self):
        widget = QWidget()
        main_layout = QVBoxLayout()

        # Header
        header = QLabel("Arqueo por Denominaciones")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(header)

        # Add Cash Count ID display
        id_group = QGroupBox("Información del Arqueo")
        id_layout = QFormLayout()
        self.denom_cash_count_id = QLineEdit()
        self.denom_cash_count_id.setReadOnly(True)
        self.denom_cash_count_id.setText(str(self.cashbox_service.get_last_cash_count_id_service() + 1))
        id_layout.addRow("No. de Control de Caja:", self.denom_cash_count_id)
        id_group.setLayout(id_layout)
        main_layout.addWidget(id_group)

        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QFormLayout()

        # Create inputs for each denomination
        for denom_name, denom_value in self.denominations:
            group = QGroupBox(f"Denominación C${denom_name}")
            group_layout = QHBoxLayout()

            count_input = QSpinBox()
            count_input.setRange(0, 10000)
            subtotal_label = QLineEdit("0.00")
            subtotal_label.setReadOnly(True)

            self.denomination_inputs[denom_name] = {
                'count': count_input,
                'subtotal': subtotal_label,
                'value': denom_value
            }

            count_input.valueChanged.connect(
                lambda value, d=denom_name: self.update_subtotal(d))

            group_layout.addWidget(QLabel("Cantidad:"))
            group_layout.addWidget(count_input)
            group_layout.addWidget(QLabel("Subtotal:"))
            group_layout.addWidget(subtotal_label)

            group.setLayout(group_layout)
            scroll_layout.addRow(group)

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Total (outside scroll area)
        total_group = QGroupBox("Totales")
        total_layout = QFormLayout()
        self.total_cash = QLineEdit("0.00")
        self.total_cash.setReadOnly(True)
        total_layout.addRow("Total Efectivo:", self.total_cash)
        total_group.setLayout(total_layout)
        main_layout.addWidget(total_group)

        # Buttons (outside scroll area)
        button_layout = QHBoxLayout()
        self.calculate_denom_btn = QPushButton("Calcular Total")
        self.calculate_denom_btn.clicked.connect(self.calculate_denominations)
        self.save_denom_btn = QPushButton("Guardar Arqueo")
        self.save_denom_btn.clicked.connect(self.save_denominations)
        button_layout.addWidget(self.calculate_denom_btn)
        button_layout.addWidget(self.save_denom_btn)
        main_layout.addLayout(button_layout)

        widget.setLayout(main_layout)
        return widget

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

    def update_subtotal(self, denomination):
        try:
            count = self.denomination_inputs[denomination]['count'].value()
            value = self.denomination_inputs[denomination]['value']
            subtotal = count * value
            self.denomination_inputs[denomination]['subtotal'].setText(f"{subtotal:.2f}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al actualizar subtotal: {str(e)}")

    def calculate_denominations(self):
        try:
            total = 0
            for denom_data in self.denomination_inputs.values():
                count = denom_data['count'].value()
                value = denom_data['value']
                total += count * value
            
            self.total_cash.setText(f"{total:.2f}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al calcular denominaciones: {str(e)}")

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
            self.denom_cash_count_id.setText(str(new_id))  # Show current ID for denominations

            QMessageBox.information(self, "Éxito", "Registro guardado exitosamente")
            self.clear_form()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar registro: {str(e)}")

    def save_denominations(self):
        try:
            # Get the latest cash count ID from service
            cash_count_id = int(self.denom_cash_count_id.getText())

            for denom_name, denom_data in self.denomination_inputs.items():
                count = denom_data['count'].value()
                if count > 0:  # Only save if there are bills/coins
                    subtotal = float(denom_data['subtotal'].text())
                    self.cashbox_service.create_cash_count_denomination_service(
                        id_cash_count=cash_count_id,
                        denominations=denom_name,
                        count=count,
                        subtotal=subtotal
                    )

            QMessageBox.information(self, "Éxito", "Arqueo guardado exitosamente")
            self.clear_form()  # Clear form after successful save
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar arqueo: {str(e)}")

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
        
        # Update denomination tab cash count ID
        current_id = self.cashbox_service.get_last_cash_count_id_service()
        self.denom_cash_count_id.setText(str(current_id + 1))
        
        # Clear remarks
        self.remarks_input.clear()
        
        # Clear all denomination inputs
        for denom_data in self.denomination_inputs.values():
            denom_data['count'].setValue(0)
            denom_data['subtotal'].setText("0.00")
        
        # Reset total cash in denominations tab
        self.total_cash.setText("0.00")

