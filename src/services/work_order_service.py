
class WorkOrderService:
    def __init__(self, db_work_orders):
        self.db = db_work_orders

    def create_work_order(self, work_order_id, start_date, end_date, user_id, client_id, colaborador_id, total_cost=0, order_status='Abierta'):
        """Crea una nueva orden de trabajo."""
        query = '''
            INSERT INTO work_orders (work_order_id, start_date, end_date, user_id, client_id, colaborador_id, total_cost, order_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.db._execute_query(query, (work_order_id, start_date, end_date, user_id, client_id, colaborador_id, total_cost, order_status))

    def get_all_work_orders(self):
            """Obtiene todas las órdenes de trabajo."""
            return self.db.get_all_orders()

    def get_work_order(self, work_order_id):
        """Obtiene una orden de trabajo por su ID."""
        query = 'SELECT * FROM work_orders WHERE id = ?'
        return self.db._fetch_one(query, (work_order_id,))

    def update_work_order(self, work_order_id, **kwargs):
        """Actualiza una orden de trabajo."""
        columns = ', '.join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values())
        values.append(work_order_id)
        query = f'UPDATE work_orders SET {columns} WHERE id = ?'
        self.db._execute_query(query, values)

    def delete_work_order(self, work_order_id):
        """Elimina una orden de trabajo."""
        query = 'DELETE FROM work_orders WHERE id = ?'
        self.db._execute_query(query, (work_order_id,))

    def add_work_order_item(self, work_order_id, colaborator_id, services):
        """Agrega un ítem a una orden de trabajo."""
        query = '''
            INSERT INTO work_order_items (work_order_id, colaborator_id, services)
            VALUES (?, ?, ?)
        '''
        self.db._execute_query(query, (work_order_id, colaborator_id, services))

    def get_work_order_items(self, work_order_id):
        """Obtiene los ítems de una orden de trabajo."""
        query = 'SELECT * FROM work_order_items WHERE work_order_id = ?'
        return self.db._fetch_all(query, (work_order_id,))

    def close(self):
        """Cierra la conexión a la base de datos."""
        self.db.close()
