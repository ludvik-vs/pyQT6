from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QFormLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout, QDateEdit, QCheckBox
)
from PyQt6.QtCore import Qt, QDateTime
from src.services.rh_service import ColaboratorService

class CreateColaborator(QWidget):
    def __init__(self, colaborator_service: ColaboratorService):
        super().__init__()
        self.colaborator_service = colaborator_service
        self.init_ui()

    def init_ui(self):
        # Establecer el fondo del formulario como gris claro
        self.setStyleSheet("background-color: #f4f4f4;")

        # Campos del formulario
        self.nombre = QLineEdit(self)
        self.apellido = QLineEdit(self)
        self.telefono_personal = QLineEdit(self)
        self.documento_identidad = QLineEdit(self)
        self.fecha_ingreso = QDateEdit(self)
        self.fecha_ingreso.setDisplayFormat("dd/MM/yyyy HH:mm:ss AP")
        self.fecha_ingreso.setCalendarPopup(True)
        self.fecha_ingreso.setDateTime(QDateTime.currentDateTime())
        self.nombre_contacto_emergencia = QLineEdit(self)
        self.telefono_emergencia = QLineEdit(self)
        self.salario = QLineEdit(self)
        self.is_active = QCheckBox("Activo", self)
        self.is_active.setChecked(True)
        self.puesto = QLineEdit(self)
        self.fecha_nacimiento = QDateEdit(self)
        self.fecha_nacimiento.setDisplayFormat("dd/MM/yyyy HH:mm:ss AP")
        self.fecha_nacimiento.setCalendarPopup(True)
        self.fecha_nacimiento.setDateTime(QDateTime.currentDateTime())
        self.numero_seguro_social = QLineEdit(self)
        self.informacion_adicional = QLineEdit(self)

        # Botones
        self.limpiar_btn = QPushButton('Limpiar Formulario', self)
        self.alta_colaborador_btn = QPushButton('Alta de Colaborador', self)

        # Conectar botones a sus respectivas funciones
        self.limpiar_btn.clicked.connect(self.clear_form)
        self.alta_colaborador_btn.clicked.connect(self.alta_colaborador)

        # Añadir campos al layout
        layout = QFormLayout()
        layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
        layout.setVerticalSpacing(18)

        # Crear QLabels con fondo transparente
        nombre_label = QLabel("Nombres:", self)
        layout.addRow(nombre_label, self.nombre)

        apellido_label = QLabel("Apellidos:", self)
        layout.addRow(apellido_label, self.apellido)

        telefono_label = QLabel("Teléfono Personal:", self)
        layout.addRow(telefono_label, self.telefono_personal)

        documento_label = QLabel("Documento de Identidad (CEDULA):", self)
        layout.addRow(documento_label, self.documento_identidad)

        fecha_ingreso_label = QLabel("Fecha de Ingreso:", self)
        layout.addRow(fecha_ingreso_label, self.fecha_ingreso)

        contacto_emergencia_label = QLabel("Nombre Contacto Emergencia:", self)
        layout.addRow(contacto_emergencia_label, self.nombre_contacto_emergencia)

        telefono_emergencia_label = QLabel("Teléfono Emergencia:", self)
        layout.addRow(telefono_emergencia_label, self.telefono_emergencia)

        salario_label = QLabel("Salario:", self)
        layout.addRow(salario_label, self.salario)

        is_active_label = QLabel("Estado:", self)
        layout.addRow(is_active_label, self.is_active)

        puesto_label = QLabel("Puesto:", self)
        layout.addRow(puesto_label, self.puesto)

        fecha_nacimiento_label = QLabel("Fecha de Nacimiento:", self)
        layout.addRow(fecha_nacimiento_label, self.fecha_nacimiento)

        seguro_social_label = QLabel("Número de Seguro Social:", self)
        layout.addRow(seguro_social_label, self.numero_seguro_social)

        informacion_label = QLabel("Información Adicional:", self)
        layout.addRow(informacion_label, self.informacion_adicional)

        # Crear un layout horizontal para los botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(60)
        button_layout.addWidget(self.limpiar_btn)
        button_layout.addWidget(self.alta_colaborador_btn)

        # Añadir el layout de botones al layout principal
        layout.addRow(button_layout)

        self.setLayout(layout)

        # Label para mostrar el resultado de la operación
        self.result_label = QLabel(self)
        self.result_label.setStyleSheet("background-color: transparent;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

    def clear_form(self):
        """Limpiar todos los campos del formulario."""
        self.nombre.clear()
        self.apellido.clear()
        self.telefono_personal.clear()
        self.documento_identidad.clear()
        self.fecha_ingreso.setDateTime(QDateTime.currentDateTime())
        self.nombre_contacto_emergencia.clear()
        self.telefono_emergencia.clear()
        self.salario.clear()
        self.is_active.setChecked(True)
        self.puesto.clear()
        self.fecha_nacimiento.setDateTime(QDateTime.currentDateTime())
        self.numero_seguro_social.clear()
        self.informacion_adicional.clear()
        self.result_label.clear()

    def alta_colaborador(self):
        """Dar de alta un colaborador y mostrar un diálogo de confirmación."""
        confirmation = QMessageBox.question(
            self,
            "Confirmar Alta",
            "¿Está seguro de que desea dar de alta este colaborador?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            nombre = self.nombre.text()
            apellido = self.apellido.text()
            telefono_personal = self.telefono_personal.text()
            documento_identidad = self.documento_identidad.text()
            fecha_ingreso = self.fecha_ingreso.date().toString("yyyy-MM-dd")
            nombre_contacto_emergencia = self.nombre_contacto_emergencia.text()
            telefono_emergencia = self.telefono_emergencia.text()
            fecha_baja = ""
            salario = self.salario.text()
            is_active = self.is_active.isChecked()
            puesto = self.puesto.text()
            fecha_nacimiento = self.fecha_nacimiento.date().toString("yyyy-MM-dd")
            numero_seguro_social = self.numero_seguro_social.text()
            informacion_adicional = self.informacion_adicional.text()

            try:
                self.colaborator_service.create_colaborator(
                    nombre, apellido, telefono_personal, documento_identidad,
                    fecha_ingreso, nombre_contacto_emergencia, telefono_emergencia,
                    fecha_baja, float(salario), is_active, puesto, fecha_nacimiento,
                    numero_seguro_social, informacion_adicional
                )
                self.clear_form()
                self.result_label.setStyleSheet("color: green;")
                self.result_label.setText("Colaborador dado de alta exitosamente.")
            except Exception as e:
                self.clear_form()
                self.result_label.setStyleSheet("color: red;")
                self.result_label.setText(f"Error al dar de alta el colaborador: {str(e)}")
        else:
            self.clear_form()
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Alta del colaborador Cancelada.")
