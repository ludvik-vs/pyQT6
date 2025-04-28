import sqlite3
from src.db.database_manager import DatabaseManager

class DatabaseClient(DatabaseManager):
    def __init__(self):
        super().__init__()
        if not self.tables_exist_and_have_records():
            self.create_client_table()
            #self.insert_default_clients()

    def create_client_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_1 TEXT,
                contact_2 TEXT,
                email TEXT NOT NULL,
                numero_ruc TEXT,
                nombre_empresa TEXT,
                sincronizado INTEGER DEFAULT 0
            )
        '''
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query)

    def insert_default_clients(self):
        """Insertar clientes predeterminados."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO clients (name, contact_1, contact_2, email, numero_ruc, nombre_empresa) VALUES (?, ?, ?, ?, ?, ?)",
                           ("Pedro Picapiedra", "123-456-7890", "987-654-3210", "peter_rok@example.com", "123456789", "Roca Dura S.A."))

    def create_client(self, name, contact_1, contact_2, email, numero_ruc, nombre_empresa):
        """Crear un nuevo cliente."""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO clients (name, contact_1, contact_2, email, numero_ruc, nombre_empresa)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, contact_1, contact_2, email, numero_ruc, nombre_empresa))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad: {e}")
            return False
        except Exception as e:
            print(f"Error al crear cliente: {e}")
            return False

    def get_all_clients(self):
        """Obtener todos los clientes."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM clients')
        return cursor.fetchall()
    
    def get_client_by_id(self, client_id):
        """Obtener un cliente por ID."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE id=?', (client_id,))
        return cursor.fetchone()

    def update_client_by_id(self, client_id, name=None, contact_1=None, contact_2=None, email=None, numero_ruc=None, nombre_empresa=None):
        """Actualizar los datos de un cliente por ID."""
        cursor = self.conn.cursor()
        query = 'UPDATE clients SET '
        params = []
        if name is not None:
            query += 'name=?, '
            params.append(name)
        if contact_1 is not None:
            query += 'contact_1=?, '
            params.append(contact_1)
        if contact_2 is not None:
            query += 'contact_2=?, '
            params.append(contact_2)
        if email is not None:
            query += 'email=?, '
            params.append(email)
        if numero_ruc is not None:
            query += 'numero_ruc=?, '
            params.append(numero_ruc)
        if nombre_empresa is not None:
            query += 'nombre_empresa=?, '
            params.append(nombre_empresa)

        # Remove the trailing comma and space
        query = query.rstrip(', ')

        query += ' WHERE id=?'
        params.append(client_id)

        try:
            cursor.execute(query, tuple(params))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            return False

    def remove_client(self, client_id):
        """Eliminar un cliente por ID."""
        cursor = self.conn.cursor()
        try:
            cursor.execute('DELETE FROM clients WHERE id=?', (client_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False
