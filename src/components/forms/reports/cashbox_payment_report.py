from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QDateEdit, QPushButton,
    QHeaderView, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class CashboxPaymentReportForm(QWidget):
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
        self.setWindowTitle("Reporte por Método de Pago")
        self.resize(800, 600)

    def setup_table(self):
        headers = ["Método de Pago", "Total Monto"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_report_data(self):
        try:
            fecha_inicio = self.start_date_filter.date().toString("yyyy-MM-dd")
            fecha_fin = self.end_date_filter.date().toString("yyyy-MM-dd")

            results = self.cashbox_service.cashbox_filter_and_totalize_per_efectivo_service(fecha_inicio, fecha_fin)
            # Parse JSON string to dictionary
            import json
            results_dict = json.loads(results)
            self.display_results(results_dict)

        except Exception as e:
            print(f"Error al cargar los datos: {str(e)}")
            # Clear the display when there's an error
            self.table.setRowCount(0)
            self.ax.clear()
            self.canvas.draw()

    def display_results(self, results):
        self.table.setRowCount(0)  # Clear existing rows

        if not results:
            print("No se encontraron registros con los filtros especificados")
            return

        detalle_movimiento = results.get("detalle_movimiento", [])
        totales_por_efectivo = results.get("totales_por_efectivo", {})

        for row_num, row_data in enumerate(detalle_movimiento):
            self.table.insertRow(row_num)
            for col_num, value in enumerate([
                row_data["metodo_pago"],
                row_data["total_monto"]
            ]):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_num, col_num, item)

        self.plot_pie_chart(totales_por_efectivo)

    def plot_pie_chart(self, totales_por_efectivo):
        self.ax.clear()
        
        labels = list(totales_por_efectivo.keys())
        sizes = list(totales_por_efectivo.values())
        
        # Create pie chart
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Set title
        self.ax.set_title('Distribución por Método de Pago')
        
        # Adjust layout
        self.figure.tight_layout()
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