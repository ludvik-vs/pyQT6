# Eliminar importaciones no utilizadas
# from datetime import datetime  # No se utiliza
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QSpinBox, QDoubleSpinBox, QMessageBox, QGroupBox,
    QTabWidget, QScrollArea, QDateEdit, QTextEdit
)
from PyQt6.QtCore import QDate  # Qt no se utiliza

class CashBalanceForm(QWidget):
    def __init__(self, auth_service, cashbox_service):
        super().__init__()
        self.auth_service = auth_service
        self.cashbox_service = cashbox_service
        self.current_user = self.auth_service.get_current_user()

        # NIO denominations
        self.nio_denominations = [
            ('1000', 1000), ('500', 500), ('200', 200),
            ('100', 100), ('50', 50), ('20', 20),
            ('10', 10), ('5', 5), ('1', 1),
            ('0.5', 0.5), ('0.25', 0.25), ('0.1', 0.1),
            ('0.05', 0.05), ('0.01', 0.01)
        ]

        # USD denominations
        self.usd_denominations = [
            ('100', 100), ('50', 50), ('20', 20),
            ('10', 10), ('5', 5), ('1', 1)
        ]

        self.nio_inputs = {}
        self.usd_inputs = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel("Arqueo De Efectivo")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(header)

        # User info
        user_group = QGroupBox("Información De Referencia")
        user_layout = QFormLayout()

        # ID Referenicia del Arqueo
        self.reference_id_input = QLineEdit()
        self.reference_id_input.setText(str(self.cashbox_service.get_last_cash_count_id_service() + 1))
        user_layout.addRow("ID Referencia:", self.reference_id_input)

        self.user_id_input = QLineEdit()
        self.user_id_input.setReadOnly(True)
        if self.current_user:
            self.user_id_input.setText(str(self.current_user.user_id))

        self.username_input = QLineEdit()
        self.username_input.setReadOnly(True)
        if self.current_user:
            self.username_input.setText(self.current_user.username)

        user_layout.addRow("ID Cajero:", self.user_id_input)
        user_layout.addRow("Nombre Cajero:", self.username_input)

        user_group.setLayout(user_layout)
        layout.addWidget(user_group)

        # Date and Exchange Rate
        date_exchange_group = QGroupBox("Fecha y Tipo de Cambio")
        date_exchange_layout = QFormLayout()

        # Date input
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        date_exchange_layout.addRow("Fecha:", self.date_input)

        # Exchange rate input
        self.exchange_rate = QDoubleSpinBox()
        self.exchange_rate.setRange(1, 100)
        self.exchange_rate.setDecimals(2)
        self.exchange_rate.setValue(36.62)  # Default exchange rate
        self.exchange_rate.valueChanged.connect(self.update_totals)
        date_exchange_layout.addRow("Tipo de Cambio USD:", self.exchange_rate)

        date_exchange_group.setLayout(date_exchange_layout)
        layout.addWidget(date_exchange_group)

        # Create tabs for NIO and USD
        tabs = QTabWidget()

        # NIO Tab
        nio_tab = QWidget()
        nio_layout = QVBoxLayout()

        # Create scroll area for NIO
        nio_scroll = QScrollArea()
        nio_scroll.setWidgetResizable(True)
        nio_content = QWidget()
        nio_scroll_layout = QFormLayout()

        # Create inputs for each NIO denomination
        for denom_name, denom_value in self.nio_denominations:
            group = QGroupBox(f"Denominación C${denom_name}")
            group_layout = QHBoxLayout()

            count_input = QSpinBox()
            count_input.setRange(0, 10000)
            subtotal_label = QLineEdit("0.00")
            subtotal_label.setReadOnly(True)

            self.nio_inputs[denom_name] = {
                'count': count_input,
                'subtotal': subtotal_label,
                'value': denom_value
            }

            count_input.valueChanged.connect(
                lambda value, d=denom_name: self.update_nio_subtotal(d))

            group_layout.addWidget(QLabel("Cantidad:"))
            group_layout.addWidget(count_input)
            group_layout.addWidget(QLabel("Subtotal:"))
            group_layout.addWidget(subtotal_label)

            group.setLayout(group_layout)
            nio_scroll_layout.addRow(group)

        nio_content.setLayout(nio_scroll_layout)
        nio_scroll.setWidget(nio_content)
        nio_layout.addWidget(nio_scroll)

        # NIO Total
        nio_total_group = QGroupBox("Total Córdobas")
        nio_total_layout = QFormLayout()
        self.total_nio = QLineEdit("0.00")
        self.total_nio.setReadOnly(True)
        nio_total_layout.addRow("Total C$:", self.total_nio)
        nio_total_group.setLayout(nio_total_layout)
        nio_layout.addWidget(nio_total_group)

        nio_tab.setLayout(nio_layout)
        tabs.addTab(nio_tab, "Córdobas (NIO)")

        # USD Tab
        usd_tab = QWidget()
        usd_layout = QVBoxLayout()

        # Create scroll area for USD
        usd_scroll = QScrollArea()
        usd_scroll.setWidgetResizable(True)
        usd_content = QWidget()
        usd_scroll_layout = QFormLayout()

        # Create inputs for each USD denomination
        for denom_name, denom_value in self.usd_denominations:
            group = QGroupBox(f"Denominación US${denom_name}")
            group_layout = QHBoxLayout()

            count_input = QSpinBox()
            count_input.setRange(0, 10000)
            subtotal_label = QLineEdit("0.00")
            subtotal_label.setReadOnly(True)

            self.usd_inputs[denom_name] = {
                'count': count_input,
                'subtotal': subtotal_label,
                'value': denom_value
            }

            count_input.valueChanged.connect(
                lambda value, d=denom_name: self.update_usd_subtotal(d))

            group_layout.addWidget(QLabel("Cantidad:"))
            group_layout.addWidget(count_input)
            group_layout.addWidget(QLabel("Subtotal US$:"))
            group_layout.addWidget(subtotal_label)

            group.setLayout(group_layout)
            usd_scroll_layout.addRow(group)

        usd_content.setLayout(usd_scroll_layout)
        usd_scroll.setWidget(usd_content)
        usd_layout.addWidget(usd_scroll)

        # USD Total
        usd_total_group = QGroupBox("Total Dólares")
        usd_total_layout = QFormLayout()
        self.total_usd = QLineEdit("0.00")
        self.total_usd.setReadOnly(True)
        self.total_usd_converted = QLineEdit("0.00")
        self.total_usd_converted.setReadOnly(True)
        usd_total_layout.addRow("Total US$:", self.total_usd)
        usd_total_layout.addRow("Total US$ en C$:", self.total_usd_converted)
        usd_total_group.setLayout(usd_total_layout)
        usd_layout.addWidget(usd_total_group)

        usd_tab.setLayout(usd_layout)
        tabs.addTab(usd_tab, "Dólares (USD)")

        layout.addWidget(tabs)

        # Grand Total (outside tabs)
        grand_total_group = QGroupBox("Total General")
        grand_total_layout = QFormLayout()
        self.grand_total = QLineEdit("0.00")
        self.grand_total.setReadOnly(True)
        grand_total_layout.addRow("Total Efectivo (C$):", self.grand_total)
        grand_total_group.setLayout(grand_total_layout)
        layout.addWidget(grand_total_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.calculate_btn = QPushButton("Calcular Totales")
        self.calculate_btn.clicked.connect(self.calculate_all)
        self.save_btn = QPushButton("Guardar Arqueo")
        self.save_btn.clicked.connect(self.save_denominations)
        self.clear_btn = QPushButton("Limpiar Formulario")
        self.clear_btn.clicked.connect(self.clear_form)

        button_layout.addWidget(self.calculate_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_nio_subtotal(self, denomination):
        try:
            count = self.nio_inputs[denomination]['count'].value()
            value = self.nio_inputs[denomination]['value']
            subtotal = count * value
            self.nio_inputs[denomination]['subtotal'].setText(f"{subtotal:.2f}")
            self.calculate_nio_total()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al actualizar subtotal NIO: {str(e)}")

    def update_usd_subtotal(self, denomination):
        try:
            count = self.usd_inputs[denomination]['count'].value()
            value = self.usd_inputs[denomination]['value']
            subtotal = count * value
            self.usd_inputs[denomination]['subtotal'].setText(f"{subtotal:.2f}")
            self.calculate_usd_total()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al actualizar subtotal USD: {str(e)}")

    def calculate_nio_total(self):
        try:
            total = 0
            for denom_data in self.nio_inputs.values():
                count = denom_data['count'].value()
                value = denom_data['value']
                total += count * value

            self.total_nio.setText(f"{total:.2f}")
            self.update_totals()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al calcular total NIO: {str(e)}")

    def calculate_usd_total(self):
        try:
            total = 0
            for denom_data in self.usd_inputs.values():
                count = denom_data['count'].value()
                value = denom_data['value']
                total += count * value

            self.total_usd.setText(f"{total:.2f}")

            # Convert to NIO
            exchange_rate = self.exchange_rate.value()
            converted = total * exchange_rate
            self.total_usd_converted.setText(f"{converted:.2f}")

            self.update_totals()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al calcular total USD: {str(e)}")

    def update_totals(self):
        try:
            nio_total = float(self.total_nio.text())
            usd_converted = float(self.total_usd_converted.text())
            grand_total = nio_total + usd_converted
            self.grand_total.setText(f"{grand_total:.2f}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al actualizar totales: {str(e)}")

    def calculate_all(self):
        self.calculate_nio_total()
        self.calculate_usd_total()
        self.update_totals()

    def save_denominations(self):
        cash_count_id = self.reference_id_input.text()
        rate = self.exchange_rate.value()
        current_user_id = self.user_id_input.text()

        try:
            if not self.current_user:
                QMessageBox.warning(self, "Error", "No hay usuario autenticado")
                return

            # Save NIO denominations
            for denom_name, denom_data in self.nio_inputs.items():
                count = denom_data['count'].value()
                if count > 0:
                    subtotal = float(denom_data['subtotal'].text())
                    self.cashbox_service.create_cash_count_denomination_service(
                        id_cash_count=cash_count_id,
                        id_user_cashier=current_user_id,
                        nio_denominations=denom_name,
                        us_denominations=None,
                        exchange_rate=rate,
                        count=count,
                        subtotal=subtotal
                    )

            # Save USD denominations
            for denom_name, denom_data in self.usd_inputs.items():
                count = denom_data['count'].value()
                if count > 0:  # Only save if there are bills/coins
                    subtotal = float(denom_data['subtotal'].text())
                    self.cashbox_service.create_cash_count_denomination_service(
                        id_cash_count=cash_count_id,
                        id_user_cashier=current_user_id,
                        nio_denominations=None,
                        us_denominations=denom_name,
                        exchange_rate=rate,
                        count=count,
                        subtotal=subtotal
                    )

            QMessageBox.information(self, "Éxito", "Arqueo guardado exitosamente")
            self.clear_form()  # Clear form after successful save
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar arqueo: {str(e)}")

    def clear_form(self):
        """Clear all form inputs and reset to default values"""
        # Reset date to current date
        self.date_input.setDate(QDate.currentDate())

        # Reset totals
        self.total_nio.setText("0.00")
        self.total_usd.setText("0.00")
        self.total_usd_converted.setText("0.00")
        self.grand_total.setText("0.00")

        # Clear all NIO denomination inputs
        for denom_data in self.nio_inputs.values():
            denom_data['count'].setValue(0)
            denom_data['subtotal'].setText("0.00")

        # Clear all USD denomination inputs
        for denom_data in self.usd_inputs.values():
            denom_data['count'].setValue(0)
            denom_data['subtotal'].setText("0.00")
