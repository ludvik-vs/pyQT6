import sqlite3
from src.db.database_manager import DatabaseManager

class DatabaseClient(DatabaseManager):
    def __init__(self):
        super().__init__()
        if not self.tables_exist_and_have_records():
            self.create_client_table()
            self.insert_default_clients()

    def create_client_table(self):
        """Crear la tabla de clientes."""
        query = '''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_1 TEXT,
                contact_2 TEXT,
                email TEXT NOT NULL
            )
        '''
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query)

    def insert_default_clients(self):
        """Insertar clientes predeterminados."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO clients (name, contact_1, contact_2, email) VALUES (?, ?, ?, ?)",
                           ("Pedro Picapiedra", "123-456-7890", "987-654-3210", "peter_rok@example.com"))

    def create_client(self, name, contact_1, contact_2, email):
        """Crear un nuevo cliente."""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO clients (name, contact_1, contact_2, email)
                VALUES (?, ?, ?, ?)
            ''', (name, contact_1, contact_2, email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_client(self, email):
        """Obtener los datos del cliente por correo electrónico."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, name, contact_1, contact_2, email FROM clients WHERE email = ?
        ''', (email,))
        return cursor.fetchone()

    def get_all_clients(self):
        """Obtener todos los clientes de la base de datos."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, name, contact_1, contact_2, email FROM clients")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener todos los clientes: {e}")
            return None

    def get_client_by_id(self, client_id):
        """Obtener datos del cliente por ID desde la base de datos."""
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, name, contact_1, contact_2, email FROM clients WHERE id = ?"
            cursor.execute(query, (client_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener cliente por ID: {e}")
            return None

    def remove_client(self, id):
        """Eliminar un cliente por id."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM clients WHERE id = ?
            ''', (id,))
            return cursor.rowcount > 0

    def update_client_by_id(self, client_id, name=None, contact_1=None, contact_2=None, email=None):
        """Actualizar los datos de un cliente por ID."""
        with self.conn:
            cursor = self.conn.cursor()
            updates = []
            params = []

            if name is not None:
                updates.append("name = ?")
                params.append(name)
            if contact_1 is not None:
                updates.append("contact_1 = ?")
                params.append(contact_1)
            if contact_2 is not None:
                updates.append("contact_2 = ?")
                params.append(contact_2)
            if email is not None:
                updates.append("email = ?")
                params.append(email)

            params.append(client_id)
            query = f"UPDATE clients SET {', '.join(updates)} WHERE id = ?"

            cursor.execute(query, tuple(params))
            return cursor.rowcount > 0
