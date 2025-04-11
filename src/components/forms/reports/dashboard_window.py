from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QDateEdit, QPushButton, QFrame, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPalette, QColor

class DashboardWindow(QMainWindow):
    def __init__(self, work_order_service, cashbox_service):
        super().__init__()
        self.work_order_service = work_order_service
        self.cashbox_service = cashbox_service
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Dashboard de Análisis Financiero")
        self.setMinimumSize(1200, 800)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)

        title = QLabel("Panel de Control Financiero")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Análisis de Órdenes de Trabajo y Movimientos Financieros")
        subtitle.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 16px;
                padding: 5px;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_widget)

        # Date range selection with better styling
        date_widget = QWidget()
        date_widget.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                color: #2c3e50;
                font-weight: bold;
            }
            QDateEdit {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                min-width: 150px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        date_layout = QHBoxLayout(date_widget)
        date_layout.setContentsMargins(20, 10, 20, 10)

        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())

        refresh_btn = QPushButton("Actualizar Dashboard")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.update_dashboard)

        date_layout.addWidget(QLabel("Fecha Inicio:"))
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("Fecha Fin:"))
        date_layout.addWidget(self.end_date)
        date_layout.addWidget(refresh_btn)
        date_layout.addStretch()

        main_layout.addWidget(date_widget)

        # Stats section title
        stats_title = QLabel("Estadísticas Generales")
        stats_title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        stats_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(stats_title)

        # Stats grid with improved styling
        stats_widget = QWidget()
        self.stats_layout = QGridLayout(stats_widget)
        self.stats_layout.setSpacing(15)
        main_layout.addWidget(stats_widget)

        # Create stat boxes
        self.create_stat_boxes()

        main_layout.addStretch()

    def create_stat_boxes(self):
        self.stat_boxes = {
            'open_orders': self.create_stat_box(
                "Órdenes Abiertas", "0",
                "#e74c3c", "Órdenes de trabajo actualmente en proceso"
            ),
            'closed_orders': self.create_stat_box(
                "Órdenes Cerradas", "0",
                "#27ae60", "Órdenes completadas y facturadas"
            ),
            'cancelled_orders': self.create_stat_box(
                "Órdenes Anuladas", "0",
                "#95a5a6", "Órdenes canceladas o anuladas"
            ),
            'open_amount': self.create_stat_box(
                "Monto Órdenes Abiertas", "C$ 0.00",
                "#f39c12", "Valor total de órdenes en proceso"
            ),
            'closed_amount': self.create_stat_box(
                "Monto Órdenes Cerradas", "C$ 0.00",
                "#2ecc71", "Valor total de órdenes completadas"
            ),
            'total_discounts': self.create_stat_box(
                "Total Descuentos", "0",
                "#9b59b6", "Número y monto total de descuentos"
            ),
            'total_discount_amount': self.create_stat_box(
                "Monto Total Descuentos", "C$ 0.00",
                "#9b59b6", "Valor monetario total de descuentos"
            ),
            'total_payments': self.create_stat_box(
                "Total Pagos", "C$ 0.00",
                "#3498db", "Monto total de pagos recibidos"
            ),
            'cash_payments': self.create_stat_box(
                "Pagos en Efectivo", "C$ 0.00",
                "#16a085", "Total de pagos recibidos en efectivo"
            ),
            'card_payments': self.create_stat_box(
                "Pagos con Tarjeta", "C$ 0.00",
                "#8e44ad", "Total de pagos recibidos con tarjeta"
            )
        }

        positions = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]

        for (key, box), pos in zip(self.stat_boxes.items(), positions):
            self.stats_layout.addWidget(box, *pos)

    def create_stat_box(self, title, value, color, description):
        box = QFrame()
        box.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        box.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 15px;
                padding: 15px;
                border: 2px solid {color};
            }}
            QLabel {{
                color: #2c3e50;
            }}
        """)

        layout = QVBoxLayout(box)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"""
            font-weight: bold;
            color: {color};
            font-size: 14px;
            padding-bottom: 5px;
        """)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px 0;
        """)
        value_label.setObjectName("value_label")  # Set an object name to find it later

        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            color: #7f8c8d;
            font-size: 12px;
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(desc_label)

        return box

    def update_dashboard(self):
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        # Get statistics from services
        order_stats = self.work_order_service.get_dashboard_statistics(start_date, end_date)

        if order_stats and 'orders_stats' in order_stats:
            stats = order_stats['orders_stats']

            # Update order statistics with None value handling
            self.update_stat_box('open_orders', str(stats[0] if stats[0] is not None else 0))
            self.update_stat_box('closed_orders', str(stats[1] if stats[1] is not None else 0))
            self.update_stat_box('cancelled_orders', str(stats[2] if stats[2] is not None else 0))
            self.update_stat_box('open_amount', f"C$ {stats[3]:,.2f}" if stats[3] is not None else "C$ 0.00")
            self.update_stat_box('closed_amount', f"C$ {stats[4]:,.2f}" if stats[4] is not None else "C$ 0.00")

        # Get discount statistics
        discounts = self.cashbox_service.get_discounts_in_date_range(start_date, end_date)
        if discounts:
            self.update_stat_box('total_discounts', str(len(discounts)))

        # Get payment statistics
        if order_stats and 'payment_stats' in order_stats:
            payment_stats = order_stats['payment_stats']
            total_payments = sum(stat[1] for stat in payment_stats)
            cash_payments = sum(stat[1] for stat in payment_stats if stat[3] == 'efectivo')
            card_payments = sum(stat[1] for stat in payment_stats if stat[3] == 'tarjeta')

            self.update_stat_box('total_payments', f"C$ {total_payments:,.2f}")
            self.update_stat_box('cash_payments', f"C$ {cash_payments:,.2f}")
            self.update_stat_box('card_payments', f"C$ {card_payments:,.2f}")

        # Get discount statistics with amounts
        discount_stats = self.cashbox_service.get_total_discounts_amount_service(start_date, end_date)
        if discount_stats:
            total_discounts = discount_stats[0] if discount_stats[0] is not None else 0
            total_discount_amount = discount_stats[1] if discount_stats[1] is not None else 0.0

            self.update_stat_box('total_discounts', str(total_discounts))
            self.update_stat_box('total_discount_amount', f"C$ {total_discount_amount:,.2f}")

    def update_stat_box(self, key, value):
        if key in self.stat_boxes:
            value_label = self.stat_boxes[key].findChild(QLabel, "value_label")
            if value_label:
                value_label.setText(value)
