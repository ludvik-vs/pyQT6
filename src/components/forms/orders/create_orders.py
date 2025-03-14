from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QDoubleSpinBox, QLabel, QHBoxLayout, QDateTimeEdit, QMessageBox
)
from PyQt6.QtCore import QDateTime
from src.components.custom.cq_divisor import CQDivisor
from src.components.custom.cq_services_list import CQServicesList

class Order:
    _instance = None

    def __new__(cls, order_id=None, client_id=None, colaborator_id=None, user_id=None, services=None, start_date=None, end_date=None, status=None, total_cost=None):
        if cls._instance is None:
            cls._instance = super(Order, cls).__new__(cls)
            cls._instance.order_id = order_id
            cls._instance.client_id = client_id
            cls._instance.colaborator_id = colaborator_id
            cls._instance.user_id = user_id
            cls._instance.services = services
            cls._instance.start_date = start_date
            cls._instance.end_date = end_date
            cls._instance.status = status
            cls._instance.total_cost = total_cost
        return cls._instance

    def __init__(self, order_id=None, client_id=None, colaborator_id=None, user_id=None, services=None, start_date=None, end_date=None, status=None, total_cost=None):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.order_id = order_id
            self.client_id = client_id
            self.colaborator_id = colaborator_id
            self.user_id = user_id
            self.services = services
            self.start_date = start_date
            self.end_date = end_date
            self.status = status
            self.total_cost = total_cost

    def __str__(self):
        return (f"Orden {self.order_id} - Cliente {self.client_id} - Colaborador {self.colaborator_id} - "
                f"Usuario {self.user_id} - Servicios {self.services} - Inicio {self.start_date} - "
                f"Fin {self.end_date} - Estatus {self.status} - Costo Total {self.total_cost}")

order_instance = Order()

class CrearOrdenForm(QWidget):

    def __init__(self, current_user_data, aunth_service, client_service, colaborator_service, work_order_service):
        super().__init__()
        self.aunth_service = aunth_service
        self.client_service = client_service
        self.colaborator_service = colaborator_service
        self.work_order_service = work_order_service
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
        id_usuario = self.current_user_data.user_id
        order_instance.user_id = id_usuario
        self.usuario_id_label = QLabel(f"Registrado por: {nombre_usuario}  ✅", self)
        layout.addRow(self.usuario_id_label)
        layout.addRow(CQDivisor())

        # Servicios
        self.services_list = CQServicesList([])
        self.services_list.services_updated.connect(self.update_services)
        layout.addRow(self.services_list)

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
        self.procesar_btn.clicked.connect(self.procesar_orden)

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
        self.colaborador_id_input.clear()
        self.costo_total_servicios_input.setValue(0.00)
        self.datos_cliente.setText("No hay cliente asignado 🔴")
        self.datos_cliente.setStyleSheet("font-size: 12px; color: orange;")
        self.datos_colaborador.setText("No hay trabajador asignado 🔴")
        self.datos_colaborador.setStyleSheet("font-size: 12px; color: orange;")
        self.fecha_recepcion_input.setDateTime(QDateTime.currentDateTime())
        self.fecha_entrega_input.setDateTime(QDateTime.currentDateTime())
        self.services_list.clear()

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
            # Inyectar client_id en order_intance
            order_instance.client_id = cliente_data['id']
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
            # Inyectar colaborador_id en order_intance
            order_instance.colaborator_id = colaborador_data[0]
            # Inyectar en el campo self.datos_colaborador
            self.datos_colaborador.setText(datos_formateados)
            self.datos_colaborador.setStyleSheet("font-size: 12px; color: #4BB543;")
        else:
            self.datos_colaborador.setText("Colaborador no encontrado")

        print("Cargando datos de colaborador...")

    def update_services(self, services):
            """Actualizar la lista de servicios en el formulario."""
            order_instance.services = eval(services)

    def procesar_orden(self):

        numero_de_orden = self.orden_input.text()
        id_colaborator = self.colaborador_id_input.text()

        # Validate required fields
        if not self.orden_input.text():
            QMessageBox.critical(self, "Error", "Número de orden no ingresado.")
            return

        if not self.client_id_input.text():
            QMessageBox.critical(self, "Error", "ID del cliente no ingresado.")
            return

        if not self.colaborador_id_input.text():
            QMessageBox.critical(self, "Error", "ID del colaborador no ingresado.")
            return

        if not self.services_list.get_services():
            QMessageBox.critical(self, "Error", "No hay servicios seleccionados.")
            return

        # Update the instance of Order with the form data
        order_instance.start_date = self.fecha_recepcion_input.dateTime().toString("yyyy-MM-dd HH:mm")
        order_instance.end_date = self.fecha_entrega_input.dateTime().toString("yyyy-MM-dd HH:mm")
        order_instance.total_cost = self.costo_total_servicios_input.value()
        order_instance.status = self.order_status.text()
        order_instance.services = self.services_list.get_services()  # Obtain services

        try:
            # Create the work order using the data from order_instance
            self.work_order_service.create_work_order(
                numero_de_orden,
                order_instance.start_date,
                order_instance.end_date,
                order_instance.user_id,
                order_instance.client_id,
                order_instance.colaborator_id,
                order_instance.total_cost,
                order_instance.status
            )
            # Add items to the work order
            try:
                self.work_order_service.add_work_order_item(numero_de_orden, id_colaborator, str(order_instance.services))
                QMessageBox.information(self, "Éxito", f"Orden de trabajo {numero_de_orden} creada exitosamente.")
                self.clear_form()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al agregar ítems a la orden: {e}")
                self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al procesar la orden: {e}")
            self.clear_form()
