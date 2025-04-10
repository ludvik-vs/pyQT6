from datetime import datetime
from PyQt6.QtWidgets import (
    QMessageBox,
    QTextEdit,
    QWidget,
    QFormLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QComboBox,
    QSpinBox
)
from src.components.custom.cq_divisor import CQDivisor

class FormularioIngresoCaja(QWidget):
    """
    Clase Formulario de Ingreso de Caja
    """
    def __init__(
        self,
        auth_service,
        client_service,
        work_order_service,
        cashbox_service
        ):
        super().__init__()
        self.auth_service = auth_service
        self.client_service = client_service
        self.work_order_service = work_order_service
        self.cashbox_service = cashbox_service
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        # Header FormularioIngresoCaja
        self.form_header = QLabel("Registro: Ingreso De Caja")
        self.form_header.setStyleSheet(
            "font-weight: bold;"
            "font-size: 24px;"
        )
        layout.addRow(self.form_header)
        layout.addRow(CQDivisor())

        # Layut horizontal
        self.layout_horizontal = QHBoxLayout()

        # Enlazar Orden
        self.orden_btn = QPushButton("Enlazar")
        self.orden_btn.clicked.connect(self.cargar_orden)
        self.orden_input = QLineEdit()
        self.orden_input.setPlaceholderText("Ingrese el número de orden")
        self.layout_horizontal.addWidget(self.orden_input)
        self.layout_horizontal.addWidget(self.orden_btn)
        layout.addRow(self.layout_horizontal)
        layout.addRow(CQDivisor())
        # ------------------------------------------------------
        self.order_data_label = QLabel("")
        layout.addRow(self.order_data_label)
        self.setLayout(layout)
        layout.addRow(CQDivisor())
        self.fecha_payment_label = QLabel("Fecha del Pago:")
        self.fecha_payment_input = QLineEdit()
        date_now = datetime.now()

        self.fecha_payment_input.setText(date_now.strftime("%Y-%m-%d"))
        self.fecha_payment_input.setReadOnly(True)
        layout.addRow(self.fecha_payment_label, self.fecha_payment_input)

        self.payment_type_label = QLabel("Tipo de Pago:")
        self.payment_type_input = QComboBox()
        self.payment_type_input.addItems(["Efectivo", "Tarjeta", "Transferencia", "Cheque", "Deposito", "Otro"])
        layout.addRow(self.payment_type_label, self.payment_type_input)

        self.reference_label = QLabel("Registrado por:")
        nombre_usuario = self.auth_service.get_current_user()
        self.user_log_register_input = QLineEdit(f"{nombre_usuario.username}")
        self.user_log_register_input.setReadOnly(True)
        layout.addRow(self.reference_label, self.user_log_register_input)

        self.paymetn_mount_label = QLabel("Monto | Cantidad (C$):")
        # Monto input
        self.payment_mount_input = QSpinBox()
        self.payment_mount_input.setRange(0, 1000000)
        self.payment_mount_input.setValue(0)
        layout.addRow(self.paymetn_mount_label, self.payment_mount_input)

        # Movimiento input
        self.movimiento_label = QLabel("Movimiento:")
        self.movimiento_input = QComboBox()
        self.load_movimientos()
        layout.addRow(self.movimiento_label, self.movimiento_input)

        self.comentario_label = QLabel("Comentario:")
        self.comentario_input = QTextEdit()
        layout.addRow(self.comentario_label, self.comentario_input)
        layout.addRow(CQDivisor())
        # ---------------------------------------------------------------------
        self.h_btns_layout = QHBoxLayout()

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.guardar_pago)
        self.clean_button = QPushButton("Limpiar")
        self.clean_button.clicked.connect(self.limpiar_formulario)
        self.h_btns_layout.setSpacing(60)
        self.h_btns_layout.addWidget(self.clean_button)
        self.h_btns_layout.addWidget(self.save_button)
        # ---------------------------------------------------------------------
        layout.addRow(self.h_btns_layout)

    def load_movimientos(self):
        try:
            movimientos = self.cashbox_service.read_all_movimientos_service()
            for movimiento in movimientos:
                if movimiento[2].lower() == 'ingreso':
                    self.movimiento_input.addItem(f"{movimiento[0]} - {movimiento[1]}", movimiento[0])
        except Exception as e:
            QMessageBox().warning(self, "Error", f"Error al cargar movimientos: {e}")

    def get_curret_user(self):
        current_user = self.auth_service.get_current_user()
        return current_user

    def cargar_orden(self):
        numero_orden = self.orden_input.text()
        if numero_orden:
            orden = self.work_order_service.get_work_order(numero_orden)
            if orden:
                self.order_data_label.setText(f'''
                Número de Orden: {orden[1]}
                Fecha: {orden[2]}
                ID Cliente: {orden[4]}
                Monto Facturado: {orden[7]}
                Estado: {orden[8]}
                ''')
                # Validar el estado de la orden
                if orden[8].lower() == "cerrada":
                    self.save_button.setVisible(False)
                else:
                    self.save_button.setVisible(True)
            else:
                QMessageBox().warning(self, "Error", "Orden no encontrada")
        else:
            QMessageBox().warning(self, "Alerta", "Ingrese el número de orden")

    def guardar_pago(self):
        numero_orden = self.orden_input.text()
        order_data = self.order_data_label.text()
        paymet_date = self.fecha_payment_input.text()
        paymet_type =  self.payment_type_input.currentText().lower()
        user_log_register_input = self.user_log_register_input.text()
        monto = self.payment_mount_input.value()
        comentario = self.comentario_input.toPlainText()
        movimiento_id = self.movimiento_input.currentData()

        if numero_orden:
            orden = self.work_order_service.get_work_order(numero_orden)
            if orden:
                try:
                    #work_order_id, payment_date, payment_method, payment, user_log_registration, note
                    self.work_order_service.set_work_order_payment(
                        numero_orden,
                        paymet_date,
                        paymet_type,
                        user_log_register_input,
                        monto,
                        comentario,
                    )
                    # Guardar en caja
                    # fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id
                    self.cashbox_service.create_cashbox_entry_service(
                        paymet_date,
                        comentario,
                        monto,
                        'ingreso',
                        paymet_type,
                        movimiento_id,
                        user_log_register_input,
                        numero_orden
                    )
                    QMessageBox().information(self, "Éxito", "Ingreso de caja registrado correctamente")
                except Exception as e:
                    QMessageBox().warning(self, "Error", f"Error no se realizo registro en caja: {e}")

                self.limpiar_formulario()
            else:
                QMessageBox().warning(self, "Error", "Orden no encontrada")
        else:
            QMessageBox().warning(self, "Alerta", "Ingrese el número de orden")

    def limpiar_formulario(self):
        self.order_data_label.setText("")
        self.orden_input.clear()
        self.payment_mount_input.setValue(0)
        self.comentario_input.clear()

    def cancelar_ingreso(self):
        self.close()
