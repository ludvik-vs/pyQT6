from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QApplication,
    QStyle
    )
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from src.components.widgets.tree_menu.tree_menu import TreeMenu

class AsideWidget(QWidget):
    def __init__(self, logs_service, auth_service):
        super().__init__()
        self.logs_service = logs_service
        self.auth_service = auth_service
        self.setStyleSheet("background-color: #fafafc; padding: 1px")
        self.init_ui()

        # Conectar la señal de autenticación
        self.auth_service.user_authenticated.connect(self.update_user_interface)
        self.update_user_interface(auth_service.get_current_user())

    def init_ui(self):

        self.main_layout = QVBoxLayout()
        self.sec_layout = QHBoxLayout()

        self.username_label = QLabel("Cargando...")
        close_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton )
        self.logout_button = QPushButton()
        self.logout_button.setIcon(close_icon)
        self.logout_button.setIconSize(QSize(20, 20))
        self.logout_button.setStyleSheet(
            """
                padding: 0px;
                margin: 0px;
                max-width: 40px;
                min-height: 20px;
            """
        )
        self.logout_button.setToolTip("Salir")
        self.sec_layout.addWidget(self.logout_button)
        self.sec_layout.addWidget(self.username_label)

        # Conectar el botón de cerrar sesión
        self.logout_button.clicked.connect(self.cerrar_sesion)

        # Agregar el layout secundario al layout principal
        self.main_layout.addLayout(self.sec_layout)

        # Crear una instancia de TreeMenu
        self.tree_menu = TreeMenu()
        self.main_layout.addWidget(self.tree_menu)

        # Asegurarse de que el QTreeView ocupe todo el espacio disponible
        self.main_layout.setStretchFactor(self.tree_menu, 1)

        self.setLayout(self.main_layout)

    def update_user_interface(self, user):
        if user:
            username = user.username if user.username else "Usuario Desconocido"
            self.username_label.setText(f"😀 Bienvenido: 🔹 {username} ")
            user_access = user.access if user.access else []
            self.tree_menu.set_user_access(user_access)
        else:
            self.username_label.setText("Usuario Desconocido")
            self.tree_menu.set_user_access([])

    def cerrar_sesion(self):
        self.auth_service.logout()
        username = self.auth_service.get_current_user().username if self.auth_service.get_current_user() else "Usuario Desconocido"
        self.logs_service.register_activity(username, "Cierre de sesión")
        QApplication.quit()
