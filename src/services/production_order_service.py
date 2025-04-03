from PyQt6.QtCore import pyqtSignal, QObject
from src.db.db_operations.db_productions_orders import DatabaseProductionOrders

class ProductionOrderService(QObject):
    order_created = pyqtSignal(dict)
    order_updated = pyqtSignal(dict)
    order_closed = pyqtSignal(str)
    order_activated = pyqtSignal(str)
    order_canceled = pyqtSignal(str)

    def __init__(self, db_manager: DatabaseProductionOrders):
        super().__init__()
        self.db_manager = db_manager

    def create_production_order(
        self, work_order_id,
        start_date,
        end_date,
        colaborador_id,
        client_id,
        product_id,
        quantity,
        order_status,
        tasks_details,
        note
    ):
        """Crear una nueva orden de producción."""
        self.db_manager.create_production_order(
            work_order_id, start_date, end_date, colaborador_id, client_id, product_id, quantity, order_status, tasks_details, note
        )
        order_data = {
            "work_order_id": work_order_id,
            "start_date": start_date,
            "end_date": end_date,
            "colaborador_id": colaborador_id,
            "client_id": client_id,
            "product_id": product_id,
            "quantity": quantity,
            "order_status": order_status,
            "tasks_details": tasks_details,
            "note": note
        }
        self.order_created.emit(order_data)

    def get_all_orders(self):
        """Obtener todas las órdenes de producción."""
        orders = self.db_manager.get_all_orders()
        return [
            {
                "id": order[0],
                "work_order_id": order[1],
                "start_date": order[2],
                "end_date": order[3],
                "colaborador_id": order[4],
                "client_id": order[5],
                "product_id": order[6],
                "quantity": order[7],
                "order_status": order[8],
                "tasks_details": order[9],
                "note": order[10]
            }
            for order in orders
        ]

    def get_production_order_details(self, work_order_id):
        """Obtener detalles de una orden de producción por ID de orden de trabajo."""
        order = self.db_manager.get_production_order_details(work_order_id)
        if order:
            return {
                "id": order[0],
                "work_order_id": order[1],
                "start_date": order[2],
                "end_date": order[3],
                "colaborador_id": order[4],
                "client_id": order[5],
                "product_id": order[6],
                "quantity": order[7],
                "order_status": order[8],
                "tasks_details": order[9],
                "note": order[10]
            }
        return None

    def update_production_order(
        self,
        work_order_id,
        start_date,
        end_date,
        colaborador_id,
        client_id,
        product_id,
        quantity,
        order_status,
        tasks_details,
        note
    ):
        """Actualizar una orden de producción."""
        if self.db_manager.update_production_order(
            work_order_id, start_date, end_date, colaborador_id, client_id, product_id, quantity, order_status, tasks_details, note
        ):
            updated_order_data = self.get_production_order_details(work_order_id)
            self.order_updated.emit(updated_order_data)
            return True
        return False

    def close_production_order(self, work_order_id):
        """Cerrar una orden de producción."""
        self.db_manager.close_production_order(work_order_id)
        self.order_closed.emit(work_order_id)

    def activate_production_order(self, work_order_id):
        """Activar una orden de producción."""
        self.db_manager.activate_production_order(work_order_id)
        self.order_activated.emit(work_order_id)

    def cancel_production_order(self, work_order_id):
        """Cancelar una orden de producción."""
        self.db_manager.cancel_production_order(work_order_id)
        self.order_canceled.emit(work_order_id)
