from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QTextEdit, QPushButton, QMessageBox, QScrollArea, QFrame)
from datetime import datetime

class ColaboratorRegister(QWidget):
    def __init__(self, logs_service, auth_service, colaborator_service):
        super().__init__()
        self.logs_service = logs_service
        self.auth_service = auth_service
        self.current_username_data = self.auth_service.get_current_user()
        self.service = colaborator_service
        self.initUI()

    def initUI(self):
        # Layout principal
        main_layout = QHBoxLayout()

        # Columna izquierda: Información del colaborador
        left_layout = QVBoxLayout()

        # ID del colaborador y botón de carga
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID del Colaborador")
        left_layout.addWidget(self.id_input)

        self.load_button = QPushButton("Cargar Datos", self)
        self.load_button.clicked.connect(self.load_colaborator_data)
        left_layout.addWidget(self.load_button)

        # Card con información del colaborador
        self.info_card = QFrame(self)
        self.info_card.setFrameShape(QFrame.Shape.Box)
        self.info_card_layout = QVBoxLayout()

        self.nombre_label = QLabel("Nombre: ", self)
        self.apellido_label = QLabel("Apellido: ", self)
        self.telefono_label = QLabel("Teléfono: ", self)
        self.documento_label = QLabel("Documento: ", self)
        self.fecha_ingreso_label = QLabel("Fecha de Ingreso: ", self)
        self.puesto_label = QLabel("Puesto: ", self)
        self.salario_label = QLabel("Salario: ", self)

        self.info_card_layout.addWidget(self.nombre_label)
        self.info_card_layout.addWidget(self.apellido_label)
        self.info_card_layout.addWidget(self.telefono_label)
        self.info_card_layout.addWidget(self.documento_label)
        self.info_card_layout.addWidget(self.fecha_ingreso_label)
        self.info_card_layout.addWidget(self.puesto_label)
        self.info_card_layout.addWidget(self.salario_label)

        self.info_card.setLayout(self.info_card_layout)
        left_layout.addWidget(self.info_card)

        # Formulario de registro
        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Ingrese un nuevo Registro")
        left_layout.addWidget(self.description_input)

        self.register_button = QPushButton("Registrar", self)
        self.register_button.clicked.connect(self.register_record)
        left_layout.addWidget(self.register_button)

        main_layout.addLayout(left_layout)

        # Columna derecha: Listado de registros
        right_layout = QVBoxLayout()
        self.registers_scroll_area = QScrollArea(self)
        self.registers_scroll_area.setWidgetResizable(True)
        self.registers_content = QWidget()
        self.registers_layout = QVBoxLayout(self.registers_content)
        self.registers_scroll_area.setWidget(self.registers_content)
        right_layout.addWidget(self.registers_scroll_area)

        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Registro de Colaborador')

    def load_colaborator_data(self):
        colaborator_id = self.id_input.text()
        if colaborator_id:
            colaborator = self.service.get_colaborator_by_id(colaborator_id)
            if colaborator:
                # Acceder a los elementos de la tupla por índice
                self.nombre_label.setText(f"Nombre: {colaborator[1]}")
                self.apellido_label.setText(f"Apellido: {colaborator[2]}")
                self.telefono_label.setText(f"Teléfono: {colaborator[3]}")
                self.documento_label.setText(f"Documento: {colaborator[4]}")
                self.fecha_ingreso_label.setText(f"Fecha de Ingreso: {colaborator[5]}")
                self.puesto_label.setText(f"Puesto: {colaborator[11]}")
                self.salario_label.setText(f"Salario: {colaborator[9]}")

                # Cargar registros del colaborador
                self.load_registers(colaborator_id)
            else:
                QMessageBox.warning(self, "Advertencia", "Colaborador no encontrado.")

    def load_registers(self, colaborator_id):
        # Limpiar registros anteriores
        for i in reversed(range(self.registers_layout.count())):
            widget = self.registers_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Cargar nuevos registros
        registers = self.service.get_all_registers(colaborator_id)
        for register in registers:
            # Crear un QFrame para cada registro
            register_card = QFrame(self)
            register_card.setFrameShape(QFrame.Shape.Box)
            register_card.setMaximumHeight(400)  # Establecer la altura máxima a 200 píxeles
            register_card.setMaximumWidth(700)  # Establecer el ancho máximo a 700 píxeles

            # Crear un layout para el QFrame
            register_card_layout = QVBoxLayout()

            # Crear un QScrollArea para permitir el desplazamiento del texto largo
            description_scroll_area = QScrollArea(self)
            description_scroll_area.setWidgetResizable(True)  # Permitir que el widget interno sea redimensionable

            # Crear un widget contenedor para el texto largo
            description_container = QWidget()
            description_layout = QVBoxLayout(description_container)

            # Agregar widgets al layout del QFrame
            fecha_label = QLabel(f"Fecha: {register[2]}", self)
            descripcion_label = QLabel(f"Descripción: {register[3]}", self)
            delete_button = QPushButton("Eliminar Registro", self)
            delete_button.clicked.connect(lambda _, rid=register[0]: self.delete_register(rid))

            # Agregar la descripción al contenedor
            description_layout.addWidget(descripcion_label)
            description_scroll_area.setWidget(description_container)

            # Agregar widgets al layout del QFrame
            register_card_layout.addWidget(fecha_label)
            register_card_layout.addWidget(description_scroll_area)
            register_card_layout.addWidget(delete_button)
            register_card.setLayout(register_card_layout)

            # Agregar el QFrame al layout principal
            self.registers_layout.addWidget(register_card)

    def register_record(self):
        colaborator_id = self.id_input.text()
        description = self.description_input.toPlainText()
        if colaborator_id and description:
            fecha = datetime.now().strftime("%Y-%m-%d")
            self.service.create_colaborator_record(colaborator_id, fecha, description)
            QMessageBox.information(self, "Éxito", "Registro creado exitosamente.")
            self.logs_service.register_activity(self.current_username_data.username,f"Agrego registro del colaborador: {self.nombre_label.text()}")
            self.description_input.clear()
            self.load_registers(colaborator_id)  # Recargar registros
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")

    def delete_register(self, register_id):
        self.service.remove_register(register_id)
        QMessageBox.information(self, "Éxito", "Registro eliminado exitosamente.")
        self.logs_service.register_activity(self.current_username_data.username,f"Elimino registro del colaborador: {self.self.nombre_label.text()}")
        self.load_registers(self.id_input.text())  # Recargar registros
