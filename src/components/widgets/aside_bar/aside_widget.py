from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from src.components.widgets.tree_menu.tree_menu import TreeMenu

class AsideWidget(QWidget):
    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.setStyleSheet("background-color: #fafafc; padding: 1px")
        self.init_ui()

        # Conectar la señal de autenticación
        self.auth_service.user_authenticated.connect(self.update_user_interface)
        self.update_user_interface(auth_service.get_current_user())

    def init_ui(self):
        layout = QVBoxLayout()
        self.sec_layout = QHBoxLayout()
        self.sec_layout.setContentsMargins(0, 0, 0, 0)
        self.sec_layout.setSpacing(0)

        # Crear un QLabel para mostrar el nombre del usuario
        self.username_label = QLabel("Cargando...")
        self.logout_button = QPushButton("🚫")
        self.logout_button.setStyleSheet(
            """
                padding: 0px;
                margin: 0px;
                width: 50px;
                height: 50px;
            """
        )
        self.logout_button.setToolTip("Cerrar Sesión")
        self.sec_layout.addWidget(self.logout_button)
        self.sec_layout.addWidget(self.username_label)

        # Conectar el botón de cerrar sesión
        self.logout_button.clicked.connect(self.cerrar_sesion)

        # Agregar el layout secundario al layout principal
        layout.addLayout(self.sec_layout)

        # Crear una instancia de TreeMenu
        self.tree_menu = TreeMenu()
        layout.addWidget(self.tree_menu)

        # Asegurarse de que el QTreeView ocupe todo el espacio disponible
        layout.setStretchFactor(self.tree_menu, 1)

        self.setLayout(layout)

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
        QApplication.quit()
