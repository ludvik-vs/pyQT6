import sqlite3
from typing import List, Tuple, Any

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

    def create_tables(self, tables_creation_queries: List[str]):
        """Crear tablas usando las consultas proporcionadas."""
        if not self.conn:
            self.connect()
        with self.conn:
            cursor = self.conn.cursor()
            for query in tables_creation_queries:
                cursor.execute(query)

    def execute_query(self, query: str, params: Tuple = ()):
        """Ejecutar una consulta SQL."""
        if not self.conn:
            self.connect()
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Tuple[Any, ...]]:
        """Obtener todos los resultados de una consulta SQL."""
        if not self.conn:
            self.connect()
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query: str, params: Tuple = ()) -> Tuple[Any, ...]:
        """Obtener un solo resultado de una consulta SQL."""
        if not self.conn:
            self.connect()
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
