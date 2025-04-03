import sqlite3
from src.db.database_manager import DatabaseManager

class DatabaseProductionOrders(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.initialize_tables()

    def initialize_tables(self):
        self.create_production_orders_table()

    def create_production_orders_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS production_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_order_id TEXT NOT NULL UNIQUE,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                colaborador_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                product_id INTEGER,
                quantity INTEGER,
                order_status TEXT NOT NULL DEFAULT 'abierta' CHECK (order_status IN ('abierta', 'procesando', 'cerrada', 'anulada')),
                tasks_details TEXT NOT NULL,
                note TEXT,
                FOREIGN KEY (work_order_id) REFERENCES work_orders(work_order_id),
                FOREIGN KEY (client_id) REFERENCES clients(id),
                FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id)
            )
        '''
        self._execute_query(query)

    def get_all_orders(self):
        query = '''
            SELECT * FROM production_orders
        '''
        return self._execute_query(query).fetchall()

    def get_production_order_id(self, work_order_id):
        query = '''
            SELECT id FROM production_orders WHERE work_order_id = ?
        '''
        result = self._execute_query(query, (work_order_id,))
        return result.fetchone()

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
        query = '''
            INSERT INTO production_orders (work_order_id, start_date, end_date, colaborador_id, client_id, product_id, quantity, order_status, tasks_details, note)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        '''
        self._execute_query(query, (work_order_id, start_date, end_date, colaborador_id, client_id, product_id, quantity, order_status, tasks_details, note))
        self.conn.commit()

    def close_production_order(self, work_order_id):
        query = '''
            UPDATE production_orders SET order_status = 'cerrada' WHERE work_order_id = ?
        '''
        self._execute_query(query, (work_order_id,))
        self.conn.commit()

    def activate_production_order(self, work_order_id):
        query = '''
            UPDATE production_orders SET order_status = 'procesando' WHERE work_order_id = ?
        '''
        self._execute_query(query, (work_order_id,))
        self.conn.commit()

    def cancel_production_order(self, work_order_id):
        query = '''
            UPDATE production_orders SET order_status = 'anulada' WHERE work_order_id = ?
        '''
        self._execute_query(query, (work_order_id,))
        self.conn.commit()

    def get_production_order_details(self, work_order_id):
        query = '''
            SELECT * FROM production_orders WHERE work_order_id = ?
        '''
        result = self._execute_query(query, (work_order_id,))
        return result.fetchone()

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
        try:
            query = '''
                UPDATE production_orders SET
                    start_date = ?,
                    end_date = ?,
                    colaborador_id = ?,
                    client_id = ?,
                    product_id = ?,
                    quantity = ?,
                    order_status = ?,
                    tasks_details = ?,
                    note = ?
                WHERE work_order_id = ?
            '''
            self._execute_query(
                query,
                (
                    start_date,
                    end_date,
                    colaborador_id,
                    client_id,
                    product_id,
                    quantity,
                    order_status,
                    tasks_details,
                    note,
                    work_order_id
                )
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        except Exception as e:
            print(f"Error updating production order: {e}")
            return False
