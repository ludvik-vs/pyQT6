import sqlite3

class DatabaseManager:
    def __init__(self, db_name='src/db/database.db'):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """Conectar a la base de datos."""
        self.conn = sqlite3.connect(self.db_name)

    def close(self):
        """Cerrar la conexión con la base de datos."""
        if self.conn:
            self.conn.close()

    def create_tables(self, tables_creation_queries):
        """Crear tablas usando las consultas proporcionadas."""
        if not self.conn:
            self.connect()
        with self.conn:
            cursor = self.conn.cursor()
            for query in tables_creation_queries:
                cursor.execute(query)