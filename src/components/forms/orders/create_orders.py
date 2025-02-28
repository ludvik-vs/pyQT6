from PyQt6.QtWidgets import QWidget, QLineEdit, QFormLayout, QTextEdit, QComboBox, QPushButton, QDoubleSpinBox, QLabel

class CrearOrdenForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Establecer el fondo del formulario como transparente
        self.setStyleSheet("background-color: white;")

        # Campos del formulario
        self.orden_input = QLineEdit(self)
        self.orden_input.setMinimumWidth(600)
        self.cliente_input = QLineEdit(self)
        self.vehicle_input = QLineEdit(self)
        self.description_input = QTextEdit(self)
        self.costo_total_servicios_input = QDoubleSpinBox(self)
        self.costo_total_servicios_input.setMaximum(9999999.99)
        self.costo_total_servicios_input.setMinimum(0.00)
        self.costo_total_servicios_input.setDecimals(2)

        # Lista desplegable para seleccionar operario
        self.operarios_combo = QComboBox(self)
        self.operarios_combo.addItems(['', 'Operario1', 'Operario2', 'Operario3'])

        # Lista desplegable para seleccionar estatus de la orden
        self.estatus_combo = QComboBox(self)
        self.estatus_combo.addItems(['Pendiente', 'En Proceso', 'Completada'])

        # Tipo de pagos
        self.tipo_pago_combo = QComboBox(self)
        self.tipo_pago_combo.addItems(['Contado Efectivo', 'Contado Tarjeta', 'Contado Transferencia', 'Crédito'])

        # Añadir campos al layout
        layout = QFormLayout()
        layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
        layout.setVerticalSpacing(18)

        # Crear QLabels con fondo transparente
        orden_label = QLabel("Número de Orden:", self)
        orden_label.setStyleSheet("background-color: transparent;")
        layout.addRow(orden_label, self.orden_input)

        cliente_label = QLabel("Cliente:", self)
        cliente_label.setStyleSheet("background-color: transparent;")
        layout.addRow(cliente_label, self.cliente_input)

        vehicle_label = QLabel("Vehículo (Placa):", self)
        vehicle_label.setStyleSheet("background-color: transparent;")
        layout.addRow(vehicle_label, self.vehicle_input)

        description_label = QLabel("Descripción del Servicio:", self)
        description_label.setStyleSheet("background-color: transparent;")
        layout.addRow(description_label, self.description_input)

        operarios_label = QLabel("Operario Asignado:", self)
        operarios_label.setStyleSheet("background-color: transparent;")
        layout.addRow(operarios_label, self.operarios_combo)

        estatus_label = QLabel("Estatus de la Orden:", self)
        estatus_label.setStyleSheet("background-color: transparent;")
        layout.addRow(estatus_label, self.estatus_combo)

        costo_label = QLabel("Costo Total de Servicios:", self)
        costo_label.setStyleSheet("background-color: transparent;")
        layout.addRow(costo_label, self.costo_total_servicios_input)

        tipo_pago_label = QLabel("Tipo de Pago:", self)
        tipo_pago_label.setStyleSheet("background-color: transparent;")
        layout.addRow(tipo_pago_label, self.tipo_pago_combo)

        # Botones Procesar Orden y Limpiar Formulario
        self.procesar_btn = QPushButton('Procesar Orden', self)
        layout.addWidget(self.procesar_btn)
        self.limpiar_btn = QPushButton('Limpiar Formulario', self)
        layout.addWidget(self.limpiar_btn)

        # Conectar el botón de limpiar al método de limpieza
        self.limpiar_btn.clicked.connect(self.clear_form)

        self.setLayout(layout)

    def clear_form(self):
        """Limpiar todos los campos del formulario."""
        self.orden_input.clear()
        self.cliente_input.clear()
        self.vehicle_input.clear()
        self.description_input.clear()
        self.costo_total_servicios_input.setValue(0.00)
        self.operarios_combo.setCurrentIndex(0)
        self.estatus_combo.setCurrentIndex(0)
        self.tipo_pago_combo.setCurrentIndex(0)
