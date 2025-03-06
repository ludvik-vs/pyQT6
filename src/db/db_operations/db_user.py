import sqlite3
from src.db.database_manager import DatabaseManager

class DatabaseUser(DatabaseManager):
    def __init__(self):
        super().__init__()
        if not self.tables_exist_and_have_records():
            self.create_user_table()
            self.create_access_table()
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
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query)

    def create_access_table(self):
        """Crear la tabla de accesos."""
        query = '''
            CREATE TABLE IF NOT EXISTS user_access (
                user_id INTEGER,
                branch_name TEXT,
                sub_branch_name TEXT,
                PRIMARY KEY (user_id, branch_name, sub_branch_name),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        '''
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query)

    def grant_access(self, user_id, branch_name, sub_branch_name=None):
        """Otorgar acceso a una rama o sub-rama a un usuario."""
        with self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO user_access (user_id, branch_name, sub_branch_name)
                    VALUES (?, ?, ?)
                ''', (user_id, branch_name, sub_branch_name))
                return True
            except sqlite3.IntegrityError:
                return False

    def revoke_access(self, user_id, branch_name, sub_branch_name=None):
        """Revocar acceso a una rama o sub-rama a un usuario."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM user_access WHERE user_id = ? AND branch_name = ? AND sub_branch_name = ?
            ''', (user_id, branch_name, sub_branch_name))
            return cursor.rowcount > 0

    def get_user_access(self, user_id):
        """Obtener los accesos de un usuario."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT branch_name, sub_branch_name FROM user_access WHERE user_id = ?
        ''', (user_id,))
        return cursor.fetchall()

    def grant_all_access_to_admin(self, user_id):
        """Otorgar todos los accesos a un usuario con rol de 'admin'."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        user_role = cursor.fetchone()
        if user_role and user_role[0] == 'admin':
            all_branches = [
                '1 - Inicio',
                'Clientes',
                'Planilla',
                'Operaciones con Ordenes',
                'Operaciones de Caja',
                'Reportes Operativos',
                'Reportes Administrativos',
                'Administración de Usuarios',
                'Operaciones de Administración'
            ]
            all_sub_branches = {
                '1 - Inicio': ['ACRIL CAR'],
                'Clientes': ['Alta de Cliente', 'Operaciones con Cliente', 'Tabla de Clientes'],
                'Operaciones con Ordenes': ['Crear Orden', 'Actualizar Orden', 'Cerrar Orden'],
                'Operaciones de Caja': ['Ingresos de Caja', 'Salidas de Caja', 'Arqueo de Caja'],
                'Planilla': ['Alta de Colaborador', 'Operaciones con Colaborador', 'Detalle por Colaborador', 'Tabla Planilla'],
                'Reportes Operativos': ['RO 1', 'RO 2', 'RO 3'],
                'Reportes Administrativos': ['RA 1', 'RA 2', 'RA 3'],
                'Administración de Usuarios': ['Crear Usuario', 'Operaciones de Usuario', 'Tabla Usuario'],
                'Operaciones de Administración': ['Aprobar Descuento', 'Eliminar Orden']
            }
            with self.conn:
                for branch in all_branches:
                    # Otorgar acceso solo a la rama principal si no tiene subramas
                    if branch not in all_sub_branches:
                        self.grant_access(user_id, branch)
                    else:
                        # Otorgar acceso a cada subrama
                        for sub_branch in all_sub_branches[branch]:
                            self.grant_access(user_id, branch, sub_branch)

    def insert_default_users(self):
        """Insertar usuarios predeterminados y otorgar accesos a admin."""
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
                admin_id = cursor.lastrowid # Obtener el ID del admin insertado
                cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                ("Francisco Castillo", admin_hash, "admin"))
                cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                ("user", user_hash, "user"))
                self.grant_all_access_to_admin(admin_id) # Otorgar todos los accesos al admin

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

    def get_all_users(self):
        """Obtener todos los usuarios."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, username, role FROM users
        ''')
        users = cursor.fetchall()
        return [{"id": row[0], "username": row[1], "role": row[2]} for row in users]

    def remove_user(self, id):
        """Eliminar user por id."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM users WHERE id = ?
            ''', (id,))
            return cursor.rowcount > 0
