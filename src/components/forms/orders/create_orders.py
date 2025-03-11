from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QTextEdit, QComboBox, QPushButton, QDoubleSpinBox, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
)

class CrearOrdenForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Establecer el fondo del formulario como transparente
        self.setStyleSheet("background-color: white;")

        # Añadir campos al layout
        layout = QFormLayout()
        layout.setVerticalSpacing(18)

        # Campos del formulario
        self.orden_input = QLineEdit(self)
        self.orden_label = QLabel("Número de Orden:", self)
        layout.addRow(self.orden_label, self.orden_input)

        self.cliente_input = QLineEdit(self)
        self.cliente_label = QLabel("Cliente:", self)
        layout.addRow(self.cliente_label, self.cliente_input)

        self.vehicle_input = QLineEdit(self)
        self.vehicle_label = QLabel("Vehículo (Placa):", self)
        layout.addRow(self.vehicle_label, self.vehicle_input)

        self.description_input = QTextEdit(self)
        self.description_label = QLabel("Descripción del Servicio:", self)
        layout.addRow(self.description_label, self.description_input)

        self.costo_total_servicios_input = QDoubleSpinBox(self)
        self.costo_total_servicios_input.setMaximum(9999999.99)
        self.costo_total_servicios_input.setMinimum(0.00)
        self.costo_total_servicios_input.setDecimals(2)
        self.costo_label = QLabel("Costo Total de Servicios:", self)
        layout.addRow(self.costo_label, self.costo_total_servicios_input)

        # Lista desplegable para seleccionar operario
        self.operarios_combo = QComboBox(self)
        self.operarios_combo.addItems(['', 'Operario1', 'Operario2', 'Operario3'])
        self.operarios_label = QLabel("Operario Asignado:", self)
        layout.addRow(self.operarios_label, self.operarios_combo)

        # Lista desplegable para seleccionar estatus de la orden
        self.estatus_combo = QComboBox(self)
        self.estatus_combo.addItems(['Pendiente', 'En Proceso', 'Completada'])
        self.estatus_label = QLabel("Estatus de la Orden:", self)
        layout.addRow(self.estatus_label, self.estatus_combo)

        # Tipo de pagos
        self.tipo_pago_combo = QComboBox(self)
        self.tipo_pago_combo.addItems(['Contado Efectivo', 'Contado Tarjeta', 'Contado Transferencia', 'Crédito'])
        self.tipo_pago_label = QLabel("Tipo de Pago:", self)
        layout.addRow(self.tipo_pago_label, self.tipo_pago_combo)

        # Botones Procesar Orden y Limpiar Formulario
        self.limpiar_btn = QPushButton('Limpiar Formulario', self)
        self.procesar_btn = QPushButton('Procesar Orden', self)

        # Contenedor horizontal para los botones
        button_container = QHBoxLayout()
        button_container.setSpacing(60)
        button_container.addWidget(self.limpiar_btn)
        button_container.addWidget(self.procesar_btn)
        layout.addRow(button_container)

        # Establecer el layout principal en el widget
        self.setLayout(layout)

        # Conectar el botón de limpiar al método de limpieza
        self.limpiar_btn.clicked.connect(self.clear_form)

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
