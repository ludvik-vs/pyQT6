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

        # Header
        header = QLabel("Arqueo por Denominaciones")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(header)

        # Add Cash Count ID display
        id_group = QGroupBox("Información del Arqueo")
        id_layout = QFormLayout()
        self.denom_cash_count_id = QLineEdit()
        self.denom_cash_count_id.setReadOnly(True)
        self.denom_cash_count_id.setText(str(self.cashbox_service.get_last_cash_count_id_service() + 1))
        id_layout.addRow("No. de Control de Caja:", self.denom_cash_count_id)
        id_group.setLayout(id_layout)
        layout.addWidget(id_group)

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
        layout.addWidget(scroll)

        # Total (outside scroll area)
        total_group = QGroupBox("Totales")
        total_layout = QFormLayout()
        self.total_cash = QLineEdit("0.00")
        self.total_cash.setReadOnly(True)
        total_layout.addRow("Total Efectivo:", self.total_cash)
        total_group.setLayout(total_layout)
        layout.addWidget(total_group)

        # Buttons (outside scroll area)
        button_layout = QHBoxLayout()
        self.calculate_denom_btn = QPushButton("Calcular Total")
        self.calculate_denom_btn.clicked.connect(self.calculate_denominations)
        self.save_denom_btn = QPushButton("Guardar Arqueo")
        self.save_denom_btn.clicked.connect(self.save_denominations)
        button_layout.addWidget(self.calculate_denom_btn)
        button_layout.addWidget(self.save_denom_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

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

    def save_denominations(self):
        try:
            # Get the latest cash count ID from service
            cash_count_id = int(self.denom_cash_count_id.text())

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
        # Update denomination tab cash count ID
        current_id = self.cashbox_service.get_last_cash_count_id_service()
        self.denom_cash_count_id.setText(str(current_id + 1))

        # Clear all denomination inputs
        for denom_data in self.denomination_inputs.values():
            denom_data['count'].setValue(0)
            denom_data['subtotal'].setText("0.00")

        # Reset total cash in denominations tab
        self.total_cash.setText("0.00")