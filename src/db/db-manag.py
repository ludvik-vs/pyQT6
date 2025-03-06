import sqlite3
import hashlib

class DatabaseManager:
    def __init__(self):
        self.db_name ='src/db/database.db'
        self.conn = sqlite3.connect(self.db_name)

    def connect(self, db_name='src/db/database.db'):
        """Conectar a la base de datos y crear tablas si no existen."""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def close(self):
        """Cerrar la conexión con la base de datos."""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Crear la tabla de usuarios e insertar datos predeterminados si está vacía."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')

            # Crear la tabla de clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact_1 TEXT,
                    contact_2 TEXT,
                    email TEXT NOT NULL
                )
            ''')

            #Tabla colaboradores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS colaboradores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    telefono_personal TEXT,
                    documento_identidad TEXT,
                    fecha_ingreso DATE NOT NULL,
                    nombre_contacto_emergencia TEXT,
                    telefono_emergencia TEXT,
                    fecha_baja DATE,
                    salario REAL NOT NULL,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    puesto TEXT,
                    fecha_nacimiento DATE,
                    numero_seguro_social TEXT,
                    informacion_adicional TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS registros_colaborador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    colaborador_id INTEGER NOT NULL,
                    fecha DATE NOT NULL,
                    descripcion TEXT NOT NULL,
                    FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id)
                )
            ''')


            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                self._insert_default_users()

            cursor.execute("SELECT COUNT(*) FROM clients")
            if cursor.fetchone()[0] == 0:
                self._insert_default_clients()


    ### USER METHODS ###
    def _insert_default_users(self):
        """Insertar usuarios predeterminados."""
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
                # El nombre de usuario ya existe
                return False

    def get_user(self, username, password):
        """Obtener los datos del usuario si la autenticación es exitosa."""
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

    def hash_password(self, password):
        """Generar un hash de la contraseña."""
        salt = 'your_secret_salt'  # Puedes cambiar esto por tu propia sal
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed_password


    ### CLIENTS METHODS ###
    def _insert_default_clients(self):
        """Insertar clientes predeterminados."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO clients (name, contact_1, contact_2, email) VALUES (?, ?, ?, ?)",
                        ("Cliente Ejemplo", "123-456-7890", "987-654-3210", "ejemplo@example.com"))

    def create_client(self, name, contact_1, contact_2, email):
        """Crear un nuevo cliente."""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO clients (name, contact_1, contact_2, email)
                VALUES (?, ?, ?, ?)
            ''', (name, contact_1, contact_2, email))
            self.conn.commit()  # Asegúrate de hacer commit para guardar los cambios
            return True
        except sqlite3.IntegrityError:
            # El cliente ya existe o hay un error de integridad
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
            query = "SELECT id, name, contact_1, contact_2, email FROM clients WHERE id = ?" # Usando un marcador de posición
            cursor.execute(query, (client_id,)) # Pasando client_id como una tupla
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

            params.append(client_id) # Agrega client_id al final de la lista de parámetros.
            query = f"UPDATE clients SET {', '.join(updates)} WHERE id = ?" # Cláusula WHERE usa id

            cursor.execute(query, tuple(params))
            return cursor.rowcount > 0
