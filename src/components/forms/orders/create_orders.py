from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QTextEdit, QComboBox, QPushButton, QDoubleSpinBox, QLabel, QHBoxLayout, QFrame
)

def crear_divisor():
    """Crea y configura un QFrame como divisor horizontal."""
    divisor = QFrame()
    divisor.setFrameShape(QFrame.Shape.HLine)
    divisor.setFrameShadow(QFrame.Shadow.Sunken)
    return divisor

class CrearOrdenForm(QWidget):

    def __init__(self, current_user_data, aunth_service, client_service, colaborator_service):
        super().__init__()
        self.aunth_service = aunth_service
        self.current_user_data = current_user_data
        self.init_ui()

    def init_ui(self):
        # Establecer el fondo del formulario como transparente
        self.setStyleSheet("background-color: white;")

        # Añadir campos al layout
        layout = QFormLayout()
        layout.setVerticalSpacing(18)

        # Form Header
        self.header = QLabel("Crear Orden de Servicio", self)
        self.header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addRow(self.header)
        layout.addRow(crear_divisor())

        # Cliente
        self.client_imput_frame = QHBoxLayout()
        self.client_imput_frame.setSpacing(10)
        self.client_id_input = QLineEdit(self)
        self.client_id_input.setPlaceholderText("Ingrese el numero ID del cliente")
        self.cargarcliente_btn = QPushButton('Enlazar', self)
        self.cargarcliente_btn.clicked.connect(self.cargar_cliente)
        self.client_imput_frame.addWidget(self.client_id_input)
        self.client_imput_frame.addWidget(self.cargarcliente_btn)
        layout.addRow(self.client_imput_frame)
        self.datos_cliente = QLabel("No hay cliente asignado 🔴")
        self.datos_cliente.setStyleSheet("font-size: 12px; color: orange;")
        layout.addRow(self.datos_cliente)

        # Atendido por
        self.colaborador_imput_frame = QHBoxLayout()
        self.colaborador_imput_frame.setSpacing(10)
        self.colaborador_id_input = QLineEdit(self)
        self.colaborador_id_input.setPlaceholderText("Ingrese el numero ID del trabajador")
        self.cargarcolaborador_btn = QPushButton('Enlazar', self)
        self.cargarcolaborador_btn.clicked.connect(self.cargar_colaborador)
        self.colaborador_imput_frame.addWidget(self.colaborador_id_input)
        self.colaborador_imput_frame.addWidget(self.cargarcolaborador_btn)
        layout.addRow(self.colaborador_imput_frame)
        self.datos_colaborador = QLabel("No hay trabajador asignado 🔴")
        self.datos_colaborador.setStyleSheet("font-size: 12px; color: orange;")
        layout.addRow(self.datos_colaborador)

        # Elaborado por
        nombre_usuario = self.current_user_data.username
        self.usuario_id_label = QLabel(F"Registrado por: {nombre_usuario}  ✅", self)
        layout.addRow(self.usuario_id_label)
        layout.addRow(crear_divisor())

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

    def cargar_cliente(self):
        """Cargar los datos del cliente en el formulario."""
        print("Cargando datos de cliente...")

    def cargar_colaborador(self):
        """Cargar los datos del colaborador en el formulario."""
        print("Cargando datos de colaborador...")
