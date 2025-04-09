from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QDateEdit, QPushButton,
    QHeaderView, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class CashboxReportForm(QWidget):
    def __init__(self, cashbox_service):
        super().__init__()
        self.cashbox_service = cashbox_service
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Filter section
        filter_layout = QHBoxLayout()

        # Date filters
        start_date_label = QLabel("Fecha Inicio:")
        self.start_date_filter = QDateEdit()
        self.start_date_filter.setCalendarPopup(True)
        self.start_date_filter.setDate(QDate.currentDate().addDays(-30))

        end_date_label = QLabel("Fecha Fin:")
        self.end_date_filter = QDateEdit()
        self.end_date_filter.setCalendarPopup(True)
        self.end_date_filter.setDate(QDate.currentDate())

        # Process button
        self.process_btn = QPushButton("Procesar")
        self.process_btn.clicked.connect(self.load_report_data)

        # Clear filters button
        self.clear_btn = QPushButton("Limpiar")
        self.clear_btn.clicked.connect(self.clear_filters)

        # Export to Excel button
        self.export_btn = QPushButton("Exportar a Excel")
        self.export_btn.clicked.connect(self.export_to_excel)

        # Add widgets to filter layout
        filter_layout.addWidget(start_date_label)
        filter_layout.addWidget(self.start_date_filter)
        filter_layout.addWidget(end_date_label)
        filter_layout.addWidget(self.end_date_filter)
        filter_layout.addWidget(self.process_btn)
        filter_layout.addWidget(self.clear_btn)
        filter_layout.addWidget(self.export_btn)
        filter_layout.addStretch()

        # Table
        self.table = QTableWidget()
        self.setup_table()

        # Pie Chart
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Add layouts to main layout
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)
        self.setWindowTitle("Reporte de Caja")
        self.resize(800, 600)

    def setup_table(self):
        headers = ["Fecha", "Descripción", "Monto", "Tipo"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_report_data(self):
        try:
            fecha_inicio = self.start_date_filter.date().toString("dd-MM-yyyy")
            fecha_fin = self.end_date_filter.date().toString("dd-MM-yyyy")

            results = self.cashbox_service.cashbox_filter_and_totalize_service(fecha_inicio, fecha_fin)
            self.display_results(results)

        except Exception as e:
            print(f"Error al cargar los datos: {str(e)}")

    def display_results(self, results):
        self.table.setRowCount(0)  # Clear existing rows

        if not results:
            print("No se encontraron registros con los filtros especificados")
            return

        detalle_movimiento = results.get("detalle_movimiento", [])
        total_ingresos = results.get("total_ingresos", 0)
        total_egresos = results.get("total_egresos", 0)

        for row_num, row_data in enumerate(detalle_movimiento):
            self.table.insertRow(row_num)
            for col_num, value in enumerate([
                row_data["fecha"], row_data["descripcion"],
                row_data["monto"], row_data["tipo"]
            ]):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_num, col_num, item)

        self.plot_pie_chart(total_ingresos, total_egresos)

    def plot_pie_chart(self, total_ingresos, total_egresos):
        labels = ['Ingresos', 'Egresos']
        sizes = [total_ingresos, total_egresos]
        self.ax.clear()
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        self.canvas.draw()

    def clear_filters(self):
        self.start_date_filter.setDate(QDate.currentDate().addDays(-30))
        self.end_date_filter.setDate(QDate.currentDate())
        self.table.setRowCount(0)
        self.ax.clear()
        self.canvas.draw()

    def export_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Excel Files (*.xlsx)")
        if file_path:
            data = []
            for row in range(self.table.rowCount()):
                row_data = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else '')
                data.append(row_data)

            df = pd.DataFrame(data, columns=[self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())])
            df.to_excel(file_path, index=False)
            print(f"Datos exportados a {file_path}")
