from PyQt6.QtWidgets import (
    QWidget, 
    QLineEdit, 
    QFormLayout, 
    QPushButton, 
    QLabel, 
    QMessageBox, 
    QHBoxLayout, 
    QVBoxLayout, 
    QSizePolicy, 
    QSpacerItem, 
    QDateTimeEdit,
    QCheckBox, 
    QVBoxLayout, 
    QScrollArea
)
from PyQt6.QtCore import Qt, QDateTime
from src.services.rh_service import ColaboratorService

class ColaboratorOperations(QWidget):

    def __init__(self, colaborator_services: ColaboratorService):
        super().__init__()
        self.colaborator_services = colaborator_services
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f4f4f4;")

        # Campos del formulario
        self.colaborator_id = QLineEdit(self)
        self.nombre_colaborador = QLineEdit(self)
        self.apellido_colaborador = QLineEdit(self)
        self.telefono_personal = QLineEdit(self)
        self.documento_identidad = QLineEdit(self)
        self.fecha_ingreso = QDateTimeEdit(self)
        self.fecha_ingreso.setDisplayFormat("dd/MM/yyyy hh:mm AP")
        self.fecha_ingreso.setDateTime(QDateTime.currentDateTime())
        self.fecha_ingreso.setCalendarPopup(True)

        self.nombre_contacto_emergencia = QLineEdit(self)
        self.telefono_emergencia = QLineEdit(self)
        self.fecha_baja = QDateTimeEdit(self)
        self.fecha_baja.setDisplayFormat("dd/MM/yyyy hh:mm AP")
        self.fecha_baja.setDateTime(QDateTime.currentDateTime())
        self.fecha_baja.setCalendarPopup(True)

        self.salario = QLineEdit(self)
        self.is_active = QCheckBox(self)
        self.puesto = QLineEdit(self)
        self.fecha_nacimiento = QDateTimeEdit(self)
        self.fecha_nacimiento.setDisplayFormat("dd/MM/yyyy hh:mm AP")
        self.fecha_nacimiento.setDateTime(QDateTime.currentDateTime())
        self.fecha_nacimiento.setCalendarPopup(True)

        self.numero_seguro_social = QLineEdit(self)
        self.informacion_adicional = QLineEdit(self)

        # Botones
        self.load_btn = QPushButton('Cargar Datos', self)
        self.limpiar_btn = QPushButton('Limpiar Datos', self)
        self.actualizar_colaborador_btn = QPushButton('Actualizar', self)
        self.eliminar_colaborador_btn = QPushButton('Eliminar', self)

        # Conectar botones a sus funciones
        self.load_btn.clicked.connect(self.load_colaborator)
        self.limpiar_btn.clicked.connect(self.clear_form)
        self.actualizar_colaborador_btn.clicked.connect(self.actualizar_colaborador)
        self.eliminar_colaborador_btn.clicked.connect(self.eliminar_colaborador)

        # Create main layout
        main_layout = QVBoxLayout()
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Create container widget for the form
        container = QWidget()
        # Layout principal
        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
        form_layout.setVerticalSpacing(18)

        # Otros campos
        colaborator_id_label = QLabel("ID del Colaborador:", self)
        colaborator_id_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(colaborator_id_label, self.colaborator_id)
        form_layout.addRow(self.load_btn)
        nombre_label = QLabel("Nombre del Colaborador:", self)
        nombre_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(nombre_label, self.nombre_colaborador)

        apellido_label = QLabel("Apellido del Colaborador:", self)
        apellido_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(apellido_label, self.apellido_colaborador)

        telefono_personal_label = QLabel("Teléfono Personal:", self)
        telefono_personal_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(telefono_personal_label, self.telefono_personal)

        documento_identidad_label = QLabel("Documento de Identidad:", self)
        documento_identidad_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(documento_identidad_label, self.documento_identidad)

        fecha_ingreso_label = QLabel("Fecha de Ingreso:", self)
        fecha_ingreso_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(fecha_ingreso_label, self.fecha_ingreso)

        nombre_contacto_emergencia_label = QLabel("Nombre de Contacto de Emergencia:", self)
        nombre_contacto_emergencia_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(nombre_contacto_emergencia_label, self.nombre_contacto_emergencia)

        telefono_emergencia_label = QLabel("Teléfono de Emergencia:", self)
        telefono_emergencia_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(telefono_emergencia_label, self.telefono_emergencia)

        fecha_baja_label = QLabel("Fecha de Baja:", self)
        fecha_baja_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(fecha_baja_label, self.fecha_baja)

        salario_label = QLabel("Salario:", self)
        salario_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(salario_label, self.salario)

        is_active_label = QLabel("Activo:", self)
        is_active_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(is_active_label, self.is_active)

        puesto_label = QLabel("Puesto:", self)
        puesto_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(puesto_label, self.puesto)

        fecha_nacimiento_label = QLabel("Fecha de Nacimiento:", self)
        fecha_nacimiento_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(fecha_nacimiento_label, self.fecha_nacimiento)

        numero_seguro_social_label = QLabel("Número de Seguro Social:", self)
        numero_seguro_social_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(numero_seguro_social_label, self.numero_seguro_social)

        informacion_adicional_label = QLabel("Información Adicional:", self)
        informacion_adicional_label.setStyleSheet("background-color: transparent;")
        form_layout.addRow(informacion_adicional_label, self.informacion_adicional)

        # Añadir botones a un contenedor horizontal
        button_container = QHBoxLayout()
        button_container.addWidget(self.limpiar_btn)
        button_container.addWidget(self.actualizar_colaborador_btn)
        button_container.addWidget(self.eliminar_colaborador_btn)

        self.result_label = QLabel(self)

        # Añadir el formulario y los botones al contenedor principal
        form_layout.addRow(self.result_label)     
        # Establecer el layout del contenedor en el scroll area
        container.setLayout(form_layout)
        # Establecer el layout del scroll area en el layout principal
        scroll.setWidget(container)
        # Añadir el scroll area al layout principal
        main_layout.addWidget(scroll)
        main_layout.addLayout(button_container)

        # Añadir el layout principal al widget principal
        self.setLayout(main_layout)

        self.setWindowTitle('Operaciones de Colaborador')


    def load_colaborator(self):
        """Cargar datos del colaborador desde la base de datos usando el ID."""
        colaborator_id = self.colaborator_id.text().strip()
        if not colaborator_id:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Por favor ingrese un ID de colaborador.")
            return

        colaborator = self.colaborator_services.get_colaborator_by_id(colaborator_id)

        if colaborator:
            self.nombre_colaborador.setText(colaborator[1])
            self.apellido_colaborador.setText(colaborator[2])
            self.telefono_personal.setText(colaborator[3])
            self.documento_identidad.setText(colaborator[4])
            self.fecha_ingreso.setDateTime(QDateTime.fromString(colaborator[5], Qt.DateFormat.ISODate))
            self.nombre_contacto_emergencia.setText(colaborator[6])
            self.telefono_emergencia.setText(colaborator[7])
            if colaborator[8]:
                self.fecha_baja.setDateTime(QDateTime.fromString(colaborator[8], Qt.DateFormat.ISODate))
            
            self.salario.setText(str(colaborator[9]))
            self.is_active.setChecked(bool(colaborator[10]))
            self.puesto.setText(colaborator[11])
            self.fecha_nacimiento.setDateTime(QDateTime.fromString(colaborator[12], Qt.DateFormat.ISODate))
            
            self.numero_seguro_social.setText(colaborator[13])
            self.informacion_adicional.setText(colaborator[14])
            self.result_label.setStyleSheet("color: green;")
            self.result_label.setText("Colaborador cargado exitosamente.")
        else:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Colaborador no encontrado.")

    def clear_form(self):
        """Limpiar todos los campos del formulario."""
        self.colaborator_id.clear()
        self.nombre_colaborador.clear()
        self.apellido_colaborador.clear()
        self.telefono_personal.clear()
        self.documento_identidad.clear()
        self.fecha_ingreso.clear()
        self.nombre_contacto_emergencia.clear()
        self.telefono_emergencia.clear()
        self.fecha_baja.clear()
        self.salario.clear()
        self.is_active.setChecked(False)
        self.puesto.clear()
        self.fecha_nacimiento.clear()
        self.numero_seguro_social.clear()
        self.informacion_adicional.clear()
        self.result_label.clear()

    def actualizar_colaborador(self):
        colaborator_id_text = self.colaborator_id.text().strip()
        nombre = self.nombre_colaborador.text()
        apellido = self.apellido_colaborador.text()
        telefono_personal = self.telefono_personal.text()
        documento_identidad = self.documento_identidad.text()
        fecha_ingreso = self.fecha_ingreso.date().toString(Qt.DateFormat.ISODate)
        nombre_contacto_emergencia = self.nombre_contacto_emergencia.text()
        telefono_emergencia = self.telefono_emergencia.text()
        fecha_baja = self.fecha_baja.date().toString(Qt.DateFormat.ISODate)
        salario = self.salario.text()
        is_active = self.is_active.isChecked()
        puesto = self.puesto.text()
        fecha_nacimiento = self.fecha_nacimiento.date().toString(Qt.DateFormat.ISODate)
        numero_seguro_social = self.numero_seguro_social.text()
        informacion_adicional = self.informacion_adicional.text()

        if not colaborator_id_text:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Por favor cargue un colaborador primero.")
            return

        try:
            colaborator_id = int(colaborator_id_text)  # Convertir el ID de string a integer
        except ValueError:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("El ID del colaborador debe ser un número válido.")
            return

        confirmation = QMessageBox.question(
            self,
            "Confirmar Actualización",
            "¿Está seguro de que desea actualizar este colaborador?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            success = self.colaborator_services.update_colaborator_by_id(
                colaborator_id,
                nombre=nombre,
                apellido=apellido,
                telefono_personal=telefono_personal,
                documento_identidad=documento_identidad,
                fecha_ingreso=fecha_ingreso,
                nombre_contacto_emergencia=nombre_contacto_emergencia,
                telefono_emergencia=telefono_emergencia,
                fecha_baja=fecha_baja,
                salario=salario,
                is_active=is_active,
                puesto=puesto,
                fecha_nacimiento=fecha_nacimiento,
                numero_seguro_social=numero_seguro_social,
                informacion_adicional=informacion_adicional,
            )

            if success:
                self.clear_form()
                self.result_label.setStyleSheet("color: green;")
                self.result_label.setText("Colaborador actualizado exitosamente.")
            else:
                self.result_label.setStyleSheet("color: red;")
                self.result_label.setText("Error al actualizar el colaborador.")
        else:
            self.clear_form()
            self.result_label.setStyleSheet("color: orange;")
            self.result_label.setText("Actualización de colaborador cancelada.")

    def eliminar_colaborador(self):
        colaborator_id_text = self.colaborator_id.text().strip()

        if not colaborator_id_text:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Por favor ingrese un ID de colaborador.")
            return

        try:
            colaborator_id = int(colaborator_id_text)  # Convertir el ID de string a integer
        except ValueError:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("El ID del colaborador debe ser un número válido.")
            return

        colaborator = self.colaborator_services.get_colaborator_by_id(colaborator_id)

        if colaborator:
            confirmation = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                "¿Está seguro de que desea eliminar este colaborador?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirmation == QMessageBox.StandardButton.Yes:
                success = self.colaborator_services.remove_colaborator_by_id(colaborator_id)

                if success:
                    self.clear_form()
                    self.result_label.setStyleSheet("color: green;")
                    self.result_label.setText("Colaborador eliminado exitosamente.")
                else:
                    self.result_label.setStyleSheet("color: red;")
                    self.result_label.setText("Error al eliminar el colaborador.")
            else:
                self.clear_form()
                self.result_label.setStyleSheet("color: orange;")
                self.result_label.setText("Eliminación cancelada.")
        else:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Colaborador no encontrado.")
