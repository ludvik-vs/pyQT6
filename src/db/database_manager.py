import sys
import os
import sqlite3
import hashlib

class DatabaseManager:
    def __init__(self):
        self.base_path = os.path.dirname(sys.executable) 
        if getattr(sys, 'frozen', False):
            self.db_name = os.path.join(self.base_path, 'acrilcar_db.db')
        else:
            self.base_path = os.path.abspath(os.path.dirname(__file__))
            self.db_name = os.path.join(self.base_path, 'acrilcar_db.db')
        self.conn = sqlite3.connect(self.db_name)

    def connect(self, db_name):
        """Conectar a la base de datos."""
        self.conn = sqlite3.connect(db_name)

    def close(self):
        """Cerrar la conexión con la base de datos."""
        if self.conn:
            self.conn.close()

    def hash_password(self, password):
        """Generar un hash de la contraseña."""
        salt = 'your_secret_salt'
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed_password

    def tables_exist_and_have_records(self):
            """Verificar si las tablas existen y tienen registros."""
            with self.conn:
                cursor = self.conn.cursor()
                # Verificar la existencia de las tablas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('users', 'clients', 'colaboradores')")
                tables = cursor.fetchall()

                # Si no existen todas las tablas, devolver False
                if len(tables) < 3:
                    return False

                # Verificar si las tablas tienen registros
                cursor.execute("SELECT COUNT(*) FROM users")
                if cursor.fetchone()[0] == 0:
                    return False

                cursor.execute("SELECT COUNT(*) FROM clients")
                if cursor.fetchone()[0] == 0:
                    return False

                cursor.execute("SELECT COUNT(*) FROM colaboradores")
                if cursor.fetchone()[0] == 0:
                    return False

                return True

    def _execute_query(self, query, params=None):
        """Ejecuta una consulta SQL con parámetros opcionales."""
        with self.conn:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
