
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
        return self.db.get_work_order_id(work_order_id)

    def update_work_order(self, work_order_id, **kwargs):
        """Actualiza una orden de trabajo."""
        columns = ', '.join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values())
        values.append(work_order_id)
        query = f'UPDATE work_orders SET {columns} WHERE work_order_id = ?'
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
        cursor = self.db._execute_query(query, (work_order_id,))
        return cursor.fetchall()

    def set_work_order_payment(self, work_order_id, payment_date, payment_method, payment, user_log_registration, note):
        """Agrega un pago a una orden de trabajo."""
        # _insert_payments
        query = '''
            INSERT INTO work_order_payments (work_order_id, payment_date, payment_method, payment, user_log_registration, note)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.db._execute_query(query, (work_order_id, payment_date, payment_method, payment, user_log_registration, note))

    def get_all_paymets_for_order(self, id):
        return self.db.get_work_order_payments(id)

    def work_order_balance(self, work_order_id):
        """Calcula el saldo de una orden de trabajo."""
        order = self.get_work_order(work_order_id)
        payments = self.db.get_work_order_payments(work_order_id)
        total = order[7]
        paid = sum(payment[5] for payment in payments)
        return str(paid - total)

    def close(self):
        """Cierra la conexión a la base de datos."""
        self.db.close()

    #Reporte
    def get_open_workorders_filter_service(self):
        """Devuelve todas las órdenes de trabajo con estado 'abierta' o 'procesando'."""
        query = '''
            SELECT * FROM work_orders
            WHERE order_status IN ('abierta', 'procesando')
            ORDER BY end_date ASC
        '''
        cursor = self.db._execute_query(query)
        return cursor.fetchall()

    # Add these methods to WorkOrderService class
    def get_dashboard_statistics(self, start_date, end_date):
        """Get comprehensive dashboard statistics."""
        try:
            orders_stats = self.db.get_orders_statistics(start_date, end_date)
            payment_stats = self.db.get_payment_statistics(start_date, end_date)
            return {
                'orders_stats': orders_stats,
                'payment_stats': payment_stats
            }
        except Exception as e:
            print(f"Error getting dashboard statistics: {e}")
            return None
        
        