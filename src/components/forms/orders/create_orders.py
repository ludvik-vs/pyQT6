from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QDoubleSpinBox, QLabel, QHBoxLayout, QDateTimeEdit
)
from PyQt6.QtCore import QDateTime
from src.components.custom.cq_divisor import CQDivisor
from src.components.custom.cq_services_list import CQServicesList

class CrearOrdenForm(QWidget):

    def __init__(self, current_user_data, aunth_service, client_service, colaborator_service):
        super().__init__()
        self.aunth_service = aunth_service
        self.client_service = client_service
        self.colaborator_service = colaborator_service
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
        layout.addRow(CQDivisor())

        # Cliente
        self.client_imput_frame = QHBoxLayout()
        self.client_imput_frame.setSpacing(10)

        self.orden_input = QLineEdit(self)
        self.orden_input.setPlaceholderText("Ingrese el número de orden")
        self.orden_label = QLabel("Número de Orden:", self)
        layout.addRow(self.orden_label, self.orden_input)

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
        self.usuario_id_label = QLabel(f"Registrado por: {nombre_usuario}  ✅", self)
        layout.addRow(self.usuario_id_label)
        layout.addRow(CQDivisor())

        # Servicios
        layout.addRow(CQServicesList())

        # Fecha y hora de recepción
        self.fecha_recepcion_input = QDateTimeEdit(self)
        self.fecha_recepcion_input.setCalendarPopup(True)
        self.fecha_recepcion_input.setDateTime(QDateTime.currentDateTime())
        self.fecha_recepcion_input.setDisplayFormat("MM/dd/yyyy hh:mm AP")
        self.fecha_recepcion_label = QLabel("Fecha y Hora de Recepción:", self)
        layout.addRow(self.fecha_recepcion_label, self.fecha_recepcion_input)

        # Fecha y hora de entrega
        self.fecha_entrega_input = QDateTimeEdit(self)
        self.fecha_entrega_input.setCalendarPopup(True)
        self.fecha_entrega_input.setDateTime(QDateTime.currentDateTime())
        self.fecha_entrega_input.setDisplayFormat("MM/dd/yyyy hh:mm AP")
        self.fecha_entrega_label = QLabel("Fecha y Hora Estaimada de Entrega:", self)
        layout.addRow(self.fecha_entrega_label, self.fecha_entrega_input)

        # Lista desplegable para seleccionar estatus de la orden
        self.estatus_label = QLabel("Estatus de la Orden:", self)
        self.order_status = QLabel("Abierta")
        self.order_status.setStyleSheet("font-size: 12px; color: #4BB543;")
        layout.addRow(self.estatus_label, self.order_status)

        self.costo_total_servicios_input = QDoubleSpinBox(self)
        self.costo_total_servicios_input.setMaximum(9999999.99)
        self.costo_total_servicios_input.setMinimum(0.00)
        self.costo_total_servicios_input.setDecimals(2)
        self.costo_label = QLabel("Costo Total de Servicios:", self)
        layout.addRow(self.costo_label, self.costo_total_servicios_input)

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
        self.client_id_input.clear()
        self.description_input.clear()
        self.costo_total_servicios_input.setValue(0.00)
        self.datos_cliente.setText("No hay cliente asignado 🔴")
        self.datos_cliente.setStyleSheet("font-size: 12px; color: orange;")
        self.datos_colaborador.setText("No hay trabajador asignado 🔴")
        self.datos_colaborador.setStyleSheet("font-size: 12px; color: orange;")
        self.fecha_recepcion_input.setDateTime(QDateTime.currentDateTime())
        self.fecha_entrega_input.setDateTime(QDateTime.currentDateTime())

    def cargar_cliente(self):
        """Cargar los datos del cliente en el formulario."""
        # Obtener id del cliente desde input
        client_id = self.client_id_input.text()
        cliente_data = self.client_service.get_client_by_id(client_id)
        if cliente_data:
            # Formatear los datos del cliente
            datos_formateados = (
                f"🟢 ID: {cliente_data['id']}\n"
                f"Nombre: {cliente_data['name']}\n"
                f"Contacto 1: {cliente_data['contact_1']}\n"
                f"Email: {cliente_data['email']}"
            )
            # Inyectar en el campo self.datos_cliente
            self.datos_cliente.setText(datos_formateados)
            # Cambiar estilo a exitoso
            self.datos_cliente.setStyleSheet("font-size: 12px; color: #4BB543;")
        else:
            self.datos_cliente.setText("Cliente no encontrado")

    def cargar_colaborador(self):
        """Cargar los datos del colaborador en el formulario."""
        # Obtener id del colaborador desde input
        colaborador_id = self.colaborador_id_input.text()
        colaborador_data = self.colaborator_service.get_colaborator_by_id(colaborador_id)
        if colaborador_data:
            # Formatear los datos del colaborador
            datos_formateados = (
                f"🟢 ID: {colaborador_data[0]}\n"
                f"Nombre: {colaborador_data[1]} {colaborador_data[2]}\n"
                f"Identificación: {colaborador_data[4]}\n"
            )
            # Inyectar en el campo self.datos_colaborador
            self.datos_colaborador.setText(datos_formateados)
            self.datos_colaborador.setStyleSheet("font-size: 12px; color: #4BB543;")
        else:
            self.datos_colaborador.setText("Colaborador no encontrado")

        print("Cargando datos de colaborador...")
