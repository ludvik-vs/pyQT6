import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt

class MovimientoDialog(QDialog):
    def __init__(self, movimiento=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Movimiento de Caja")
        self.movimiento = movimiento

        self.layout = QFormLayout(self)

        self.nombre_edit = QLineEdit(self)
        self.tipo_combo = QComboBox(self)
        self.tipo_combo.addItems(["ingreso", "egreso"])
        self.descripcion_edit = QLineEdit(self)

        self.layout.addRow("Nombre:", self.nombre_edit)
        self.layout.addRow("Tipo:", self.tipo_combo)
        self.layout.addRow("Descripción:", self.descripcion_edit)

        self.save_button = QPushButton("Guardar", self)
        self.layout.addRow(self.save_button)

        self.save_button.clicked.connect(self.accept)

        if movimiento:
            # Assuming tuple order: id, nombre, tipo, descripcion
            self.nombre_edit.setText(str(movimiento[1]))
            self.tipo_combo.setCurrentText(str(movimiento[2]))
            self.descripcion_edit.setText(str(movimiento[3]))

    def get_data(self):
        return {
            "nombre": self.nombre_edit.text(),
            "tipo": self.tipo_combo.currentText(),
            "descripcion": self.descripcion_edit.text()
        }

class CashMovementForm(QMainWindow):
    def __init__(self, logs_service, cashbox_service, auth_service):
        super().__init__()
        self.logs_service = logs_service
        self.cashbox_service = cashbox_service
        self.auth_service = auth_service
        self.current_username_data = self.auth_service.get_current_user()

        self.setWindowTitle("Administrador de Movimientos de Caja")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Changed from 3 to 4 to include ID
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Tipo", "Descripción"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.layout.addWidget(self.table)

        self.add_button = QPushButton("Agregar Movimiento", self)
        self.edit_button = QPushButton("Editar Movimiento", self)
        self.delete_button = QPushButton("Eliminar Movimiento", self)

        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.delete_button)

        self.add_button.clicked.connect(self.add_movimiento)
        self.edit_button.clicked.connect(self.edit_movimiento)
        self.delete_button.clicked.connect(self.delete_movimiento)

        self.load_movimientos()

    def load_movimientos(self):
        movimientos = self.cashbox_service.read_all_movimientos_service()
        self.table.setRowCount(len(movimientos))
        for row, movimiento in enumerate(movimientos):
            # Assuming tuple order: id, nombre, tipo, descripcion
            self.table.setItem(row, 0, QTableWidgetItem(str(movimiento[0])))  # id
            self.table.setItem(row, 1, QTableWidgetItem(str(movimiento[1])))  # nombre
            self.table.setItem(row, 2, QTableWidgetItem(str(movimiento[2])))  # tipo
            self.table.setItem(row, 3, QTableWidgetItem(str(movimiento[3])))  # descripcion

    def add_movimiento(self):
        dialog = MovimientoDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.cashbox_service.create_movimiento_service(
                nombre=data["nombre"],
                tipo=data["tipo"],
                descripcion=data["descripcion"]
            )
            nombre_movimiento = data["nombre"]
            self.logs_service.register_activity(self.current_username_data.username,f"Agrego movimiento: {nombre_movimiento}")
            self.load_movimientos()

    def edit_movimiento(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un movimiento para editar.")
            return

        # Get the ID directly from the table instead of calculating it
        movimiento_id = int(self.table.item(selected_row, 0).text())
        movimiento = self.cashbox_service.read_movimiento_service(movimiento_id)

        dialog = MovimientoDialog(movimiento=movimiento, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.cashbox_service.update_movimiento_service(
                movimiento_id=movimiento_id,
                nombre=data["nombre"],
                tipo=data["tipo"],
                descripcion=data["descripcion"]
            )
            self.logs_service.register_activity(self.current_username_data.username, f'Edito movimiento: {data["nombre"]}')
            self.load_movimientos()

    def delete_movimiento(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un movimiento para eliminar.")
            return

        # Get the ID directly from the table instead of calculating it
        movimiento_id = int(self.table.item(selected_row, 0).text())
        self.cashbox_service.delete_movimiento_service(movimiento_id)
        self.logs_service.register_activity(self.current_username_data.username,f"Elimino movimiento, id: {movimiento_id}")
        self.load_movimientos()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Suponiendo que tienes instancias de CashBoxService y AuthService
    cashbox_service = CashBoxService(db_cashbox=None)  # Reemplaza con tu instancia real
    auth_service = AuthService(db_manager=None)  # Reemplaza con tu instancia real

    window = CashMovementForm(cashbox_service, auth_service)
    window.show()
    sys.exit(app.exec())
