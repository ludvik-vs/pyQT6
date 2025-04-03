from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QTextEdit
)
from src.components.custom.cq_divisor import CQDivisor
from src.components.custom.cq_messagebox import CQMessageBox

class CancelOrderForm(QWidget):
    def __init__(
        self, 
        current_user_data, 
        aunth_service, 
        work_order_service,
        production_order_service
        ):
        super().__init__()
        self.current_user_data = current_user_data
        self.aunth_service = aunth_service
        self.work_order_service = work_order_service
        self.production_order_service = production_order_service
        self.init_ui()

    def init_ui(self):
        # Establecer el fondo del formulario como transparente
        self.setStyleSheet("background-color: white;")
        
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Create container widget for the form
        container = QWidget()

        # Form layout
        self.details_layout = QFormLayout()
        #----------------------------------------
        # Form header
        self.form_header = QLabel("Cancelar Orden de Trabajo")
        self.form_header.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.details_layout.addRow(self.form_header)
        self.details_layout.addRow(CQDivisor())
        
        # Order ID
        # layout horizontal
        self.h_input_layout = QHBoxLayout()

        # Label ID
        # Input ID
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Ingrese ID de la orden")
        # Enlazar orde btn
        self.enlazar_btn = QPushButton("Enlazar")
        self.enlazar_btn.clicked.connect(self.cargar_orden)
        self.h_input_layout.addWidget(self.id_input)
        self.h_input_layout.addWidget(self.enlazar_btn)
        self.details_layout.addRow(self.h_input_layout)
        # Order Data
        self.order_info_label = QLabel("Informacion de la orden: ")
        self.details_layout.addRow(self.order_info_label)
        # User data
        self.curren_user_label = QLabel("Usuario que anula: ")
        self.current_user_input = QLabel("Nombre del usuario")
        self.details_layout.addRow(self.curren_user_label, self.current_user_input)
        # Motivo
        # Motivo Label
        self.motivo_label = QLabel("Motivo de la anulacion:")
        # Motivo texto
        self.motivo_input = QTextEdit()
        self.details_layout.addRow(self.motivo_label, self.motivo_input )
        self.details_layout.addRow(CQDivisor())

        # Botones
        # layout horizontal
        self.h_button_layout = QHBoxLayout()
        self.h_button_layout.setSpacing(60)
        # Boton de cancelar
        self.cancel_button = QPushButton("Anular Order")
        self.cancel_button.clicked.connect(self.anular_order)
        # Boton de limpiar form
        self.clear_button = QPushButton("Limpiar Formulario")
        self.clear_button.clicked.connect(self.clear_form)
        self.h_button_layout.addWidget(self.clear_button)
        self.h_button_layout.addWidget(self.cancel_button)

        #----------------------------------------
        container.setLayout(self.details_layout)
        scroll.setWidget(container)
        # Establecer el layout principal
        main_layout.addWidget(scroll)
        # Agregar el layout de botones al layout principal
        main_layout.addLayout(self.h_button_layout)
        self.setLayout(main_layout)
    
    def cargar_orden(self):
        """
        Cargar detalle de la orde y mostrar usuario actual 
        """
        order_id = self.id_input.text()
        order_data = self.work_order_service.get_work_order(order_id)
        order_status = order_data[8]
        current_user = self.current_user_data.username

        if order_status == "Cerrada":
            self.cancel_button.setVisible(False)

        if order_data:
            self.order_info_label.setText(f"""
            Nomero de order: {order_data[1]}
            Fecha de ingreso: {order_data[2]}
            Fecha de entrega: {order_data[3]}
            ID Cliente: {order_data[5]}
            Monto Factura: {order_data[7]}
            Estatus de la orden: {order_data[8]}
            """)
            self.current_user_input.setText(current_user)
        else:
            CQMessageBox().error_message("No se encontro la orden")

    def anular_order(self):
        order_id = self.id_input.text()
        text_motivo = self.motivo_input.toPlainText()
        try:
            # First verify if production order exists
            production_order = self.production_order_service.get_production_order_details(order_id)
            
            # Update work order status
            self.work_order_service.update_work_order(order_id, order_status="anulada", note=text_motivo)
            
            # Only cancel production order if it exists
            if production_order:
                self.production_order_service.cancel_production_order(order_id)
            
            CQMessageBox().info_message("Orden anulada con exito")
            self.clear_form()
            
        except Exception as e:
            CQMessageBox().error_message(f"Error al anular la orden: {str(e)}")
    
    def clear_form(self):
        self.id_input.clear()
        self.order_info_label.setText("")
    