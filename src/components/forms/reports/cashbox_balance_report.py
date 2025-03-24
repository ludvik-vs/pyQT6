from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, 
    QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QLabel, QDateEdit, QLineEdit, 
    QPushButton, QHeaderView
    )
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from src.components.custom.cq_messagebox import CQMessageBox

class CashboxReportForm(QWidget):
    def __init__(self, cashbox_service):
        super().__init__()
        self.cashbox_service = cashbox_service
        self.message_box = CQMessageBox()
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Filter section
        filter_layout = QHBoxLayout()
        
        # Date filter
        date_label = QLabel("Fecha:")
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        
        # Index filter
        index_label = QLabel("Índice:")
        self.index_filter = QLineEdit()
        
        # Search button
        self.search_btn = QPushButton("Buscar")
        self.search_btn.clicked.connect(self.load_report_data)
        
        # Clear filters button
        self.clear_btn = QPushButton("Limpiar Filtros")
        self.clear_btn.clicked.connect(self.clear_filters)
        
        # Add widgets to filter layout
        filter_layout.addWidget(date_label)
        filter_layout.addWidget(self.date_filter)
        filter_layout.addWidget(index_label)
        filter_layout.addWidget(self.index_filter)
        filter_layout.addWidget(self.search_btn)
        filter_layout.addWidget(self.clear_btn)
        filter_layout.addStretch()
        
        # Table
        self.table = QTableWidget()
        self.setup_table()
        
        # Add layouts to main layout
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
        self.setWindowTitle("Reporte de Conteo de Efectivo")
        self.resize(800, 600)

    def setup_table(self):
        headers = [
            "ID", "Fecha", "Índice", "Denominación NIO", 
            "Denominación USD", "Tipo de Cambio", 
            "Cantidad", "Subtotal", "Cajero"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
    def load_report_data(self):
        try:
            if self.date_filter.date().isValid():
                fecha_qdate = self.date_filter.date()
                fecha = fecha_qdate.toString("dd-MM-yyyy")
            index = self.index_filter.text() if self.index_filter.text() else None
            
            print(f"Fecha: {fecha}, Índice: {index}")

            if index:
                try:
                    index = int(index)
                except ValueError:
                    self.message_box.warning_message("El índice debe ser un número válido")
                    return
            
            results = self.cashbox_service.get_cash_count_report_service(fecha, index)
            print(f"RESULTADOS: {results}")

            self.table.setRowCount(0)  # Clear existing rows
            
            if not results:
                self.message_box.info_message("No se encontraron registros con los filtros especificados")
                return
                
            for row_num, row_data in enumerate(results):
                self.table.insertRow(row_num)
                for col_num, value in enumerate(row_data):
                    if col_num == 1:  # Date column
                        value = value.strftime('%d-%m-%Y') if value else ''
                    item = QTableWidgetItem(str(value) if value is not None else '')
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row_num, col_num, item)
            
            self.message_box.success_message(f"Se encontraron {self.table.rowCount()} registros")

        except Exception as e:
            self.message_box.error_message(f"Error al cargar los datos: {str(e)}")

    def clear_filters(self):
        self.date_filter.setDate(QDate.currentDate())
        self.index_filter.clear()
        self.load_report_data()