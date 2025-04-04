from src.db.database_manager import DatabaseManager

class DatabaseWorkOrder(DatabaseManager):

    def __init__(self):
        super().__init__()
        self.initialize_tables()

    def initialize_tables(self):
        """Inicializa todas las tablas necesarias."""
        self.create_work_orders_table()
        self.create_work_order_items_table()
        self.create_work_order_payments_table()

    def create_work_orders_table(self):
        """Crea la tabla de órdenes de trabajo."""
        query = '''
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_order_id TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                colaborador_id INTEGER NOT NULL,
                total_cost REAL DEFAULT 0,
                order_status TEXT NOT NULL DEFAULT 'abierta' CHECK (order_status IN ('abierta', 'procesando', 'cerrada', 'anulada')),
                note TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (client_id) REFERENCES clients(id),
                FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id)
            )
        '''
        self._execute_query(query)
        #self._insert_work_order('777', '2021-01-01', '2021-01-02', 1, 1, 1, 600, 'Abierta', "Nota Ejemplo")

    def create_work_order_items_table(self):
        """Crea la tabla de ítems de órdenes de trabajo."""
        query = '''
            CREATE TABLE IF NOT EXISTS work_order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_order_id INTEGER NOT NULL,
                colaborator_id INTEGER NOT NULL,
                services TEXT NOT NULL,
                FOREIGN KEY (work_order_id) REFERENCES work_orders(id),
                FOREIGN KEY (colaborator_id) REFERENCES colaboradores(id)
            )
        '''
        self._execute_query(query)

    def create_work_order_payments_table(self):
        """Crea la tabla de pagos de órdenes de trabajo."""
        query = '''
            CREATE TABLE IF NOT EXISTS work_order_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_order_id INTEGER NOT NULL,
                payment_date TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                payment REAL NOT NULL,
                user_log_registration INTEGER NOT NULL,
                note TEXT,
                FOREIGN KEY (user_log_registration) REFERENCES users(id),
                FOREIGN KEY (work_order_id) REFERENCES work_orders(id)
            )
        '''
        self._execute_query(query)
        # Valida si existe registro en la tabal work_order_payments
        #self._insert_payments("777", "payment_date",  "payment_method", "note",  1000.00 )

    def get_all_orders(self):
        """Devuelve todas las órdenes de trabajo."""
        query = '''
            SELECT * FROM work_orders
        '''
        cursor = self._execute_query(query)
        return cursor.fetchall()

    def get_work_order_id(self, id):
        """Obtiene una orden de trabajo por su ID."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT * FROM work_orders WHERE work_order_id = ?''', (id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener la orden de trabajo: {e}")
            raise

    def get_work_order_payments(self, id):
        """Obtiene los pagos asociados a una orden de trabajo."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT * FROM work_order_payments WHERE work_order_id = ?''', (id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener los pagos de la orden de trabajo: {e}")
            raise

    def close(self):
        self.conn.close()

    def _insert_work_order(self, work_order_id, start_date, end_date, user_id, client_id, colaborador_id, total_cost, order_status, note):
        """Registra los datos de una orden de trabajo y devuelve el ID de la orden."""
        query = '''
            INSERT INTO work_orders (work_order_id, start_date, end_date, user_id, client_id, colaborador_id, total_cost, order_status, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor = self._execute_query(query, (work_order_id, start_date, end_date, user_id, client_id, colaborador_id, total_cost, order_status, note))
        if cursor:
            return cursor.lastrowid
        else:
            return None

    def _insert_items(self, work_order_id, colaborator_id, services):
        """Registra los ítems de una orden de trabajo."""
        if work_order_id is None:
            raise ValueError("work_order_id cannot be None")

        query = '''
            INSERT INTO work_order_items (work_order_id, colaborator_id, services)
            VALUES (?, ?, ?)
        '''
        self._execute_query(query, (work_order_id, colaborator_id, services))

    def _insert_payments(self, work_order_id, payment_date, payment_method, payment, user_log_registration, note):
        """Registra los pagos de una orden de trabajo."""
        if work_order_id is None:
            raise ValueError("work_order_id cannot be None")

        query = '''
            INSERT INTO work_order_payments (work_order_id, payment_date, payment_method, payment, user_log_registration, note)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self._execute_query(query, (work_order_id, payment_date, payment_method, payment, user_log_registration, note))
