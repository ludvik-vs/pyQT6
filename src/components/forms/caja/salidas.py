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

class FormularioEgresoCaja(QWidget):
    """
    Clase Formulario de Egreso de Caja
    """
    def __init__(
        self,
        auth_service,
        work_order_service,
        cashbox_service
        ):
        super().__init__()
        self.auth_service = auth_service
        self.work_order_service = work_order_service
        self.cashbox_service = cashbox_service
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        # Header
        self.form_header = QLabel("Registro: Egreso De Caja")
        self.form_header.setStyleSheet(
            "font-weight: bold;"
            "font-size: 24px;"
        )
        layout.addRow(self.form_header)
        layout.addRow(CQDivisor())

        # Fecha
        self.fecha_payment_label = QLabel("Fecha del Egreso:")
        self.fecha_payment_input = QLineEdit()
        date_now = datetime.now()
        self.fecha_payment_input.setText(date_now.strftime("%d-%m-%Y %I:%M:%S %p"))
        self.fecha_payment_input.setReadOnly(True)
        layout.addRow(self.fecha_payment_label, self.fecha_payment_input)

        # Tipo de Pago
        self.payment_type_label = QLabel("Método de Pago:")
        self.payment_type_input = QComboBox()
        self.payment_type_input.addItems(["Efectivo", "Tarjeta", "Transferencia", "Cheque", "Deposito", "Otro"])
        layout.addRow(self.payment_type_label, self.payment_type_input)

        # Usuario que registra
        self.reference_label = QLabel("Registrado por:")
        nombre_usuario = self.auth_service.get_current_user()
        self.user_log_register_input = QLineEdit(f"{nombre_usuario.username}")
        self.user_log_register_input.setReadOnly(True)
        layout.addRow(self.reference_label, self.user_log_register_input)

        # Monto
        self.payment_mount_label = QLabel("Monto | Cantidad (C$):")
        self.payment_mount_input = QSpinBox()
        self.payment_mount_input.setRange(0, 1000000)
        self.payment_mount_input.setValue(0)
        layout.addRow(self.payment_mount_label, self.payment_mount_input)

        # Movimiento (solo mostrará movimientos tipo 'egreso')
        self.movimiento_label = QLabel("Movimiento:")
        self.movimiento_input = QComboBox()
        self.load_movimientos()
        layout.addRow(self.movimiento_label, self.movimiento_input)

        # Orden de trabajo (opcional)
        self.orden_label = QLabel("Orden de Trabajo (Opcional):")
        self.orden_input = QLineEdit()
        self.orden_input.setPlaceholderText("Número de orden (si aplica)")
        layout.addRow(self.orden_label, self.orden_input)

        # Comentario
        self.comentario_label = QLabel("Descripción del Egreso:")
        self.comentario_input = QTextEdit()
        layout.addRow(self.comentario_label, self.comentario_input)
        layout.addRow(CQDivisor())

        # Botones
        self.h_btns_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.guardar_egreso)
        self.clean_button = QPushButton("Limpiar")
        self.clean_button.clicked.connect(self.limpiar_formulario)
        self.h_btns_layout.setSpacing(60)
        self.h_btns_layout.addWidget(self.clean_button)
        self.h_btns_layout.addWidget(self.save_button)
        layout.addRow(self.h_btns_layout)

    def load_movimientos(self):
        try:
            movimientos = self.cashbox_service.read_all_movimientos_service()
            for movimiento in movimientos:
                # Solo agregar movimientos tipo 'egreso'
                if movimiento[2].lower() == 'egreso':
                    self.movimiento_input.addItem(f"{movimiento[0]} - {movimiento[1]}", movimiento[0])
        except Exception as e:
            QMessageBox().warning(self, "Error", f"Error al cargar movimientos: {e}")

    def guardar_egreso(self):
        try:
            fecha = self.fecha_payment_input.text()
            metodo_pago = self.payment_type_input.currentText().lower()
            user_id = self.user_log_register_input.text()
            monto = self.payment_mount_input.value()
            movimiento_id = self.movimiento_input.currentData()
            orden_id = self.orden_input.text() or "0"  # Si no hay orden, usar 0
            descripcion = self.comentario_input.toPlainText()

            if monto <= 0:
                QMessageBox().warning(self, "Error", "El monto debe ser mayor a 0")
                return

            if not movimiento_id:
                QMessageBox().warning(self, "Error", "Debe seleccionar un tipo de movimiento")
                return

            if not descripcion:
                QMessageBox().warning(self, "Error", "Debe ingresar una descripción")
                return

            # Guardar en caja
            self.cashbox_service.create_cashbox_entry_service(
                fecha,
                descripcion,
                monto,
                'egreso',  # Tipo fijo para este formulario
                metodo_pago,
                movimiento_id,
                user_id,
                orden_id
            )

            QMessageBox().information(self, "Éxito", "Egreso de caja registrado correctamente")
            self.limpiar_formulario()

        except Exception as e:
            QMessageBox().warning(self, "Error", f"Error al registrar egreso: {e}")

    def limpiar_formulario(self):
        date_now = datetime.now()
        self.fecha_payment_input.setText(date_now.strftime("%d-%m-%Y %I:%M:%S %p"))
        self.payment_mount_input.setValue(0)
        self.orden_input.clear()
        self.comentario_input.clear()