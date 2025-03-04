import hashlib
import sqlite3
from src.db.database_manager import DatabaseManager

class DatabaseUser(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.create_user_table()
        self.insert_default_users()

    def create_user_table(self):
        """Crear la tabla de usuarios."""
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        '''
        self.create_tables([query])

    def insert_default_users(self):
        """Insertar usuarios predeterminados si la tabla está vacía."""
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            admin_hash = self.hash_password("admin")
            user_hash = self.hash_password("user")
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                               ("admin", admin_hash, "admin"))
                cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                               ("Francisco Castillo", admin_hash, "admin"))
                cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                               ("user", user_hash, "user"))

    def hash_password(self, password):
        """Generar un hash de la contraseña."""
        salt = 'your_secret_salt'
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed_password

    def create_user(self, username, password, role):
        """Crear un nuevo usuario."""
        password_hash = self.hash_password(password)
        with self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role)
                    VALUES (?, ?, ?)
                ''', (username, password_hash, role))
                return True
            except sqlite3.IntegrityError:
                return False

    def get_user(self, username, password):
        """Obtener los datos del usuario."""
        password_hash = self.hash_password(password)
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, username, role FROM users WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        return cursor.fetchone()

    def remove_user(self, id):
        """Eliminar user por id."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM users WHERE id = ?
            ''', (id,))
            return cursor.rowcount > 0