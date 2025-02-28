from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QLineEdit, QPushButton, QLabel, QSizePolicy, QHeaderView
)
from PyQt6.QtCore import Qt
from src.services.client_service import ClientService

class ClientTableWidget(QWidget):
    def __init__(self, client_service: ClientService):
        super().__init__()
        self.client_service = client_service
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: white;")
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Campo de filtro
        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Filtrar por nombre o email...")
        self.filter_input.textChanged.connect(self.filter_table)
        layout.addWidget(self.filter_input)

        # Tabla
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Contacto 1", "Contacto 2", "Email"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Configurar el encabezado para distribuir uniformemente
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Todas las columnas se estiran uniformemente
        
        layout.addWidget(self.table, stretch=1)
        # layout.addWidget(self.table)

        # Botones de operaciones
        self.refresh_btn = QPushButton("Refrescar Lista", self)
        
        self.refresh_btn.clicked.connect(self.load_clients)
        
        layout.addWidget(self.refresh_btn)

        # Label para resultados
        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Cargar clientes inicialmente
        self.load_clients()

    def load_clients(self):
        """Cargar todos los clientes en la tabla."""
        clients = self.client_service.get_all_clients()
        self.table.setRowCount(0)  # Limpiar tabla
        
        for row, client in enumerate(clients):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(client["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(client["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(client["contact_1"] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(client["contact_2"] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(client["email"]))
        
        #self.table.resizeColumnsToContents()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.result_label.setText(f"Mostrando {len(clients)} clientes")

    def filter_table(self):
        """Filtrar la tabla basado en el texto del filtro."""
        filter_text = self.filter_input.text().lower()
        all_clients = self.client_service.get_all_clients()
        
        filtered_clients = [
            client for client in all_clients 
            if filter_text in client["name"].lower() or filter_text in client["email"].lower()
        ]
        
        self.table.setRowCount(0)
        for row, client in enumerate(filtered_clients):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(client["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(client["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(client["contact_1"] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(client["contact_2"] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(client["email"]))
        
        self.result_label.setText(f"Mostrando {len(filtered_clients)} clientes filtrados")
