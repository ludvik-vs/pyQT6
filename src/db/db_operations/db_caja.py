from src.db.database_manager import DatabaseManager

class DBCaja(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.initialize_tables()

    def initialize_tables(self):
        self.create_table_caja()

    def create_table_caja(self):
        query = """
            CREATE TABLE IF NOT EXISTS caja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                monto REAL NOT NULL,
                movimiento INTEGER NOT NULL,
                descripcion TEXT NOT NULL
            );
        """
        self._execute_query(query)

    def create_table_registros(self):
        query = """
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
            );
        """
        self._execute_query(query)
