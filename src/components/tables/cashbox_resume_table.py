from PyQt6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QDialog, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt

class CashBoxResumeTableWidget(QWidget):
    def __init__(
        self,
        current_user_data,
        aunth_service,
        client_service,
        colaborator_service,
        work_order_service,
        production_order_service,
        cashbox_service
    ):
        super().__init__()
        self.current_user_data = current_user_data
        self.aunth_service = aunth_service
        self.client_service = client_service
        self.colaborator_service = colaborator_service
        self.work_order_service = work_order_service
        self.production_order_service = production_order_service
        self.cashbox_service = cashbox_service

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Fecha", "Índice"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_widget.cellDoubleClicked.connect(self.show_detail_popup)

        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)

        # Load data into the table
        self.load_data()

    def load_data(self):
        # Fetch data from the cashbox service
        data = self.cashbox_service.get_all_index_identifiers_service()

        self.table_widget.setRowCount(len(data))
        for row_idx, record in enumerate(data):
            self.table_widget.setItem(row_idx, 0, QTableWidgetItem(record[1]))
            self.table_widget.setItem(row_idx, 1, QTableWidgetItem(str(record[2])))

    def show_detail_popup(self, row, column):
        # Get the selected record
        record = {
            "fecha": self.table_widget.item(row, 0).text(),
            "index_identifier": self.table_widget.item(row, 1).text(),
        }
        print(f"UI: {record['index_identifier']}")

        # Get count data 
        count_date = self.cashbox_service.get_cash_count_denomination_by_index_identifier_service(record["index_identifier"])

        print(f"COUNT: {count_date}")

        # Create and show the detail popup
        detail_popup = CashCountDetailPopup(record)
        detail_popup.exec()

class CashCountDetailPopup(QDialog):
    def __init__(self, record):
        super().__init__()
        self.record = record
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Detalle de Arqueo de Efectivo")
        self.layout = QVBoxLayout()

        # Display record details
        self.layout.addWidget(QLabel(f"Fecha: {self.record['fecha']}"))
        self.layout.addWidget(QLabel(f"Índice: {self.record['index_identifier']}"))

        # Add a close button
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        self.layout.addWidget(close_button)

        self.setLayout(self.layout)
