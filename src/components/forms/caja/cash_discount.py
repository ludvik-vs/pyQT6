from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QDoubleSpinBox, QLabel,
    QHBoxLayout, QVBoxLayout, QScrollArea, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt

class CashDiscountForm(QWidget):
    def __init__(self, current_user_data, work_order_service, cashbox_service):
        super().__init__()
        self.work_order_service = work_order_service
        self.current_user_data = current_user_data
        self.cashbox_service = cashbox_service
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()

        self.details_layout = QFormLayout()
        self.details_layout.setVerticalSpacing(18)

        self.fm_header = QLabel("Aplicar Descuento a Orden", self)
        self.fm_header.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.details_layout.addRow(self.fm_header)

        self.orden_input = QLineEdit(self)
        self.orden_input.setPlaceholderText("Ingrese el número de orden")
        self.details_layout.addRow("Número de Orden:", self.orden_input)

        self.cargar_orden_btn = QPushButton('Cargar Orden', self)
        self.cargar_orden_btn.clicked.connect(self.cargar_orden)
        self.details_layout.addRow(self.cargar_orden_btn)

        self.discount_date = QLineEdit()
        date_now = datetime.now()
        self.discount_date.setText(date_now.strftime("%Y-%m-%d"))
        self.discount_date.setReadOnly(True)
        self.details_layout.addRow("Fecha:", self.discount_date)

        nombre_usuario = self.current_user_data.username
        self.usuario_label = QLabel(f"Usuario actual: {nombre_usuario}  ✅", self)
        self.usuario_label.setStyleSheet("font-size: 12px; color: #4BB543;")
        self.details_layout.addRow(self.usuario_label)

        self.monto_inicial_label = QLabel("Monto Inicial (C$):", self)
        self.monto_inicial_value = QLabel("0.00", self)
        self.details_layout.addRow(self.monto_inicial_label, self.monto_inicial_value)

        self.nuevo_monto_label = QLabel("Nuevo Monto (C$):", self)
        self.nuevo_monto_input = QDoubleSpinBox(self)
        self.nuevo_monto_input.setMaximum(9999999.99)
        self.nuevo_monto_input.setMinimum(0.00)
        self.nuevo_monto_input.setDecimals(2)
        self.details_layout.addRow(self.nuevo_monto_label, self.nuevo_monto_input)

        self.aplicar_descuento_btn = QPushButton('Aplicar Descuento', self)
        self.aplicar_descuento_btn.clicked.connect(self.aplicar_descuento)
        self.details_layout.addRow(self.aplicar_descuento_btn)

        self.resultado_label = QLabel("Descuento Aplicado (C$):", self)
        self.resultado_value = QLabel("0.00", self)
        self.details_layout.addRow(self.resultado_label, self.resultado_value)

        self.descripcion_label = QLabel("Descripción:", self)
        self.descripcion_input = QTextEdit(self)
        self.descripcion_input.setPlaceholderText("Ingrese una descripción")
        self.descripcion_input.setMaximumHeight(100)
        self.details_layout.addRow(self.descripcion_label, self.descripcion_input)

        self.grabar_descuento_btn = QPushButton('Grabar Descuento', self)
        self.grabar_descuento_btn.clicked.connect(self.grabar_descuento)
        self.details_layout.addRow(self.grabar_descuento_btn)

        container.setLayout(self.details_layout)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def cargar_orden(self):
        """Cargar los datos de la orden."""
        numero_orden = self.orden_input.text()
        orden_data = self.work_order_service.get_work_order(numero_orden)

        if orden_data:
            try:
                monto_inicial = float(orden_data[7])
                self.monto_inicial_value.setText(f"{monto_inicial:.2f}")
            except (IndexError, ValueError):
                QMessageBox.critical(self, "Error", "Error al procesar los datos de la orden.")
        else:
            QMessageBox.critical(self, "Error", "Orden no encontrada.")

    def aplicar_descuento(self):
        """Aplicar el descuento a la orden."""
        try:
            monto_inicial = float(self.monto_inicial_value.text())
            nuevo_monto = self.nuevo_monto_input.value()
            descuento = monto_inicial - nuevo_monto
            self.resultado_value.setText(f"{descuento:.2f}")
        except ValueError:
            QMessageBox.critical(self, "Error", "Error al calcular el descuento.")

    def grabar_descuento(self):
        """Grabar el descuento en la base de datos."""
        id_usuario = self.current_user_data.user_id
        numero_orden = self.orden_input.text()

        try:
            descuento = float(self.resultado_value.text())
            if descuento <= 0:
                raise ValueError("El descuento debe ser mayor que cero.")

            cash_discount = self.nuevo_monto_input.value()
            monto_inicial = float(self.monto_inicial_value.text())
            discount_percentage = ((cash_discount / monto_inicial) * 100)

            if not self.descripcion_input.toPlainText():
                raise ValueError("El motivo de descuento no puede estar vacío.")

            discount_description = self.descripcion_input.toPlainText()

            self.cashbox_service.create_discount_service(
                date=datetime.now().strftime("%Y-%m-%d"),
                user_id=id_usuario,
                order_id=numero_orden,
                discount_mont=cash_discount,
                discount_percentage=discount_percentage,
                description=discount_description
            )

            self.work_order_service.update_work_order(
                work_order_id = numero_orden,
                total_cost= descuento
            )

            QMessageBox.information(self, "Éxito", "Descuento grabado exitosamente.")
            self.clean_form()  # Add this line

        except ValueError as ve:
            QMessageBox.critical(self, "Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al grabar el descuento: {e}")

    def clean_form(self):
        """Clean all form fields after successful discount registration."""
        self.orden_input.clear()
        self.monto_inicial_value.setText("0.00")
        self.nuevo_monto_input.setValue(0.00)
        self.resultado_value.setText("0.00")
        self.descripcion_input.clear()
        date_now = datetime.now()
        self.discount_date.setText(date_now.strftime("%Y-%m-%d"))
