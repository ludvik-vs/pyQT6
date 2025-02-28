from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from src.components.widgets.tree_menu.tree_menu import TreeMenu

class AsideWidget(QWidget):
    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.setStyleSheet("background-color: #fafafc; padding: 1px")
        self.init_ui()

        # Conectar la señal de autenticación
        self.auth_service.user_authenticated.connect(self.update_user_interface)

    def init_ui(self):
        layout = QVBoxLayout()

        # Crear un QLabel para mostrar el nombre del usuario
        self.username_label = QLabel("Cargando...")
        layout.addWidget(self.username_label)

        # Crear una instancia de TreeMenu
        self.tree_menu = TreeMenu()
        layout.addWidget(self.tree_menu)

        # Asegurarse de que el QTreeView ocupe todo el espacio disponible
        layout.setStretchFactor(self.tree_menu, 1)

        self.setLayout(layout)

    def update_user_interface(self, user):
        if user:
            username = user.get('username', 'Usuario Desconocido')
            self.username_label.setText(f"😀 Bienvenido: 🔹 {username} ")
            role = user.get('role', 'user')  # Obtener el rol del usuario
            self.tree_menu.set_role_visibility(role)
        else:
            self.username_label.setText("Usuario Desconocido")
