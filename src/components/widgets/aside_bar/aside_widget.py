from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QApplication,
    QStyle
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize
from src.components.widgets.tree_menu.tree_menu import TreeMenu

class AsideWidget(QWidget):

    def __init__(self, logs_service, auth_service):
        super().__init__()
        self.logs_service = logs_service
        self.auth_service = auth_service
        self.setStyleSheet("""
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 10px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
            font-weight: 700;
        """)
        self.init_ui()
        self.auth_service.user_authenticated.connect(self.update_user_interface)
        self.update_user_interface(auth_service.get_current_user())

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.sec_layout = QVBoxLayout()
        self.cls_btn_layout = QHBoxLayout()

        self.username_label = QLabel("Cargando...")
        self.username_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        # Create logout button with icon
        self.logout_button = QPushButton('Cerrar')
        self.logout_button.setIconSize(QSize(16, 16))
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.logout_button.setToolTip("Salir")
        
        # Add widgets to layouts
        self.cls_btn_layout.addWidget(self.logout_button)
        self.cls_btn_layout.addStretch()  # This pushes the button to the left
        
        self.sec_layout.addLayout(self.cls_btn_layout)
        self.sec_layout.addWidget(self.username_label)

        self.logout_button.clicked.connect(self.cerrar_sesion)

        self.main_layout.addLayout(self.sec_layout)

        self.tree_menu = TreeMenu()
        self.tree_menu.setStyleSheet("""
            QTreeView {
                background-color: #34495e;
                color: #ecf0f1;
                border: none;
            }
            QTreeView::item:selected {
                background-color: #1abc9c;
                color: #ecf0f1;
            }
            QTreeView::item:hover {
                background-color: #2980b9;
            }
        """)
        self.main_layout.addWidget(self.tree_menu)
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
        current_user = self.auth_service.get_current_user()
        username = current_user.username if current_user else "Usuario Desconocido"
        self.logs_service.register_activity(username, "Cierre de sesión")
        self.auth_service.logout()
        QApplication.quit()
