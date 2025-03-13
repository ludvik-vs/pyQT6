from src.db.database_manager import DatabaseManager

class DatabaseWorkOrders(DatabaseManager):

    def __init__(self):
        super().__init__()
        if not self.tables_exist_and_have_records():
            self.initialize_tables()

    def initialize_tables(self):
        """Inicializa todas las tablas necesarias."""
        self.create_work_orders_table()
        self.create_work_order_items_table()
        self.create_work_order_status_table()
        self.create_work_order_items_status_table()
        self.create_work_order_items_history_table()
        self.create_work_order_items_status_history_table()

    def create_work_orders_table(self):
        """Crea la tabla de órdenes de trabajo."""
        query = '''
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                order_status_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                colaborador_id INTEGER NOT NULL,
                FOREIGN KEY (order_status_id) REFERENCES work_order_status(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (client_id) REFERENCES clients(id),
                FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id)
            )
        '''
        self._execute_query(query)
        self._insert_work_order('2021-01-01', '2021-01-02', 1, 1, 1, 1)

    def create_work_order_items_table(self):
        """Crea la tabla de ítems de órdenes de trabajo."""
        query = '''
            CREATE TABLE IF NOT EXISTS work_order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_order_id INTEGER NOT NULL,
                colaborator_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (work_order_id) REFERENCES work_orders(id),
                FOREIGN KEY (colaborator_id) REFERENCES colaboradores(id)
            )
        '''
        self._execute_query(query)

    def create_work_order_status_table(self):
        """Crea la tabla de estados de órdenes de trabajo."""
        query = '''
            CREATE TABLE IF NOT EXISTS work_order_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT UNIQUE NOT NULL
            )
        '''
        self._execute_query(query)
        self._insert_initial_statuses('work_order_status', ['Abierta', 'En curso', 'Cerrada'])

    #  Inserts
    def _execute_query(self, query, params=None):
        """Ejecuta una consulta SQL con parámetros opcionales."""
        with self.conn:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor

    def _insert_work_order(self, start_date, end_date, order_status_id, user_id, client_id, colaborador_id):
        """Registra los datos de una orden de trabajo y devuelve el ID de la orden."""
        query = '''
            INSERT INTO work_orders (start_date, end_date, order_status_id, user_id, client_id, colaborador_id)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor = self._execute_query(query, (start_date, end_date, order_status_id, user_id, client_id, colaborador_id))
        order_id = cursor.lastrowid
        return order_id

    def _insert_initial_statuses(self, table_name, statuses):
        """Inserta estados iniciales en una tabla."""
        with self.conn:
            cursor = self.conn.cursor()
            for status in statuses:
                cursor.execute(f"INSERT INTO {table_name} (status) VALUES (?)", (status,))

    def _create_work_order_with_items(self, start_date, end_date, order_status_id, user_id, client_id, colaborador_id, items, insert_defaults=False):
        """Crea una orden de trabajo con múltiples ítems, incluyendo ítems por defecto opcionales."""

        query_order = '''
            INSERT INTO work_orders (start_date, end_date, order_status_id, user_id, client_id, colaborador_id)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor = self._execute_query(query_order, (start_date, end_date, order_status_id, user_id, client_id, colaborador_id))
        order_id = cursor.lastrowid

        query_item = '''
            INSERT INTO work_order_items (work_order_id, description, status)
            VALUES (?, ?, ?)
        '''

        # Insertar los ítems proporcionados
        if items:
            for item in items:
                self._execute_query(query_item, (order_id, item['description'], item['status']))

        # Insertar ítems por defecto si insert_defaults es True
        if insert_defaults:
            default_items = [
                {'description': 'Revisión general', 'status': 'Pendiente'},
                {'description': 'Limpieza básica', 'status': 'Pendiente'},
            ]
            for item in default_items:
                self._execute_query(query_item, (order_id, item['description'], item['status']))

    def close(self):
        self.conn.close()
