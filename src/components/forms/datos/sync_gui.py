import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QScrollArea, QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from src.components.forms.datos.sync_worker import GitSyncWorker

class ZincDataForm(QWidget):
    """
    Formulario para la sincronización de datos con un repositorio Git.
    
    Inputs:
        tablas (list): Lista de nombres de tablas para sincronizar
    """
    def __init__(self, tablas):
        super().__init__()
        self.tablas = tablas
        self.setWindowTitle("Sincronización de Base de Datos")
        self.default_db_path = self.get_default_db_path()
        self.setup_ui()

    def get_default_db_path(self):
        """
        Obtiene la ruta predeterminada de la base de datos.
        
        Returns:
            str: Ruta absoluta al archivo de base de datos
        """
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(base_path)))
        return os.path.join(base_path, 'acrilcar_database.db')

    def setup_ui(self):
        """
        Configura la interfaz de usuario del formulario.
        Crea y organiza todos los elementos visuales como campos de entrada,
        botones y layouts.
        """
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        main_layout = QVBoxLayout(container)
        form_layout = QFormLayout()

        self.db_path_input = QLineEdit()
        self.db_path_input.setText(self.default_db_path)
        self.db_path_input.setPlaceholderText("Ruta de la base de datos")

        self.repo_url_input = QLineEdit()
        self.repo_url_input.setText("REPOSITORIO_URL")
        self.repo_url_input.setPlaceholderText("URL del repositorio (https://github.com/usuario/repo)")

        token_layout = QHBoxLayout()
        
        self.token_input = QLineEdit()
        self.token_input.setText("TOKENSIO")
        self.token_input.setPlaceholderText("Token de GitHub")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        token_layout.addWidget(self.token_input)

        copy_button = QPushButton("Copiar")
        copy_button.setFixedWidth(60)
        copy_button.clicked.connect(self.copy_token)
        token_layout.addWidget(copy_button)

        self.toggle_button = QPushButton("👁")
        self.toggle_button.setFixedWidth(30)
        self.toggle_button.clicked.connect(self.toggle_token_visibility)
        token_layout.addWidget(self.toggle_button)

        form_layout.addRow("Base de datos:", self.db_path_input)
        form_layout.addRow("Repositorio:", self.repo_url_input)
        form_layout.addRow("Token GitHub:", token_layout)

        main_layout.addLayout(form_layout)

        self.sync_button = QPushButton("Sincronizar")
        self.sync_button.clicked.connect(self.start_sync)
        main_layout.addWidget(self.sync_button)

        scroll.setWidget(container)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

    def start_sync(self):
        """
        Inicia el proceso de sincronización.
        """
        # Validación de campos
        db_path = self.db_path_input.text().strip()
        repo_url = self.repo_url_input.text().strip()
        token = self.token_input.text().strip()
        
        # Validaciones específicas
        if not all([db_path, repo_url, token]):
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return
        
        # Validar formato de URL de GitHub
        if not repo_url.startswith("https://github.com/"):
            QMessageBox.warning(self, "Error", "La URL debe ser de GitHub (https://github.com/...)")
            return
        
        # Validar que la base de datos existe
        if not os.path.exists(db_path):
            QMessageBox.warning(self, "Error", f"Base de datos no encontrada en: {db_path}")
            return
        
        # Deshabilitar botón y mostrar estado
        self.sync_button.setEnabled(False)
        self.sync_button.setText("Sincronizando...")
        
        # Iniciar worker
        self.worker = GitSyncWorker(
            db_path=db_path,
            repo_url=repo_url,
            token=token,
            tablas=self.tablas
        )
        self.worker.finished.connect(self.on_sync_finished)
        self.worker.start()

    def on_sync_finished(self, success, message):
        """
        Manejador de evento para cuando finaliza la sincronización.
        
        Inputs:
            success (bool): True si la sincronización fue exitosa, False si falló
            message (str): Mensaje describiendo el resultado de la operación
        """
        self.sync_button.setEnabled(True)
        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.critical(self, "Error", message)

    def copy_token(self):
        """
        Copia el token de GitHub al portapapeles del sistema.
        Muestra un mensaje de confirmación al usuario.
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(self.token_input.text())
        QMessageBox.information(self, "Copiado", "Token copiado al portapapeles")

    def toggle_token_visibility(self):
        """
        Alterna la visibilidad del token entre texto plano y caracteres ocultos.
        Cambia el ícono del botón según el estado de visibilidad.
        """
        if self.token_input.echoMode() == QLineEdit.EchoMode.Password:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_button.setText("🔒")
        else:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_button.setText("👁")
