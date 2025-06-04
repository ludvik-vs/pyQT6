import sqlite3
from src.db.database_manager import DatabaseManager
from src.config.menu_structure import MenuStructure

class DatabaseUser(DatabaseManager):
    
    def __init__(self):
        super().__init__()
        if not self.tables_exist_and_have_records():
            try:
                self.create_user_table()
                print("Tabla de 'users' creada corectamente.")
            except sqlite3.OperationalError:
                print("Error al crear la tabla de usuarios.")
            
            try:
                self.create_access_table()
                print("Tabla de 'user_access' creada corectamente.")
            except sqlite3.OperationalError:
                print("Error al crear la tabla de accesos.")
    
            self.insert_default_users()
        
        # Add this line to clean up duplicates during initialization
        deleted_count = self.cleanup_duplicate_access()
        if deleted_count > 0:
            print(f"Se eliminaron {deleted_count} registros duplicados de accesos")

    def create_user_table(self):
        """Crear la tabla de usuarios."""
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                sincronizado INTEGER DEFAULT 0
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
                sincronizado INTEGER DEFAULT 0,
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
            # Check if access already exists
            cursor.execute('''
                SELECT 1 FROM user_access 
                WHERE user_id = ? AND branch_name = ? AND sub_branch_name = ?
            ''', (user_id, branch_name, sub_branch_name))
            
            if cursor.fetchone():
                return True  # Access already exists
            
            try:
                cursor.execute('''
                    INSERT INTO user_access (user_id, branch_name, sub_branch_name)
                    VALUES (?, ?, ?)
                ''', (user_id, branch_name, sub_branch_name))
                return True
            except sqlite3.IntegrityError:
                return False

    def grant_all_access_to_admin(self, user_id):
        """Otorgar todos los accesos a un usuario con rol de 'admin'."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        user_role = cursor.fetchone()
        
        if user_role and user_role[0] == 'admin':
            # First, remove any existing access
            cursor.execute("DELETE FROM user_access WHERE user_id = ?", (user_id,))
            
            all_branches = MenuStructure.get_all_branches()
            all_sub_branches = MenuStructure.get_menu_structure()
            
            with self.conn:
                for branch in all_branches:
                    if branch not in all_sub_branches:
                        self.grant_access(user_id, branch)
                    else:
                        for sub_branch in all_sub_branches[branch]:
                            self.grant_access(user_id, branch, sub_branch)

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
            all_branches = MenuStructure.get_all_branches()
            all_sub_branches = MenuStructure.get_menu_structure()
            
            with self.conn:
                for branch in all_branches:
                    if branch not in all_sub_branches:
                        self.grant_access(user_id, branch)
                    else:
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
                '''
                cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                ("Francisco Castillo", admin_hash, "admin"))
                cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                ("user", user_hash, "user"))
                '''
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

    def verify_password(self, user_id, password):
        """Verificar la contraseña de un usuario."""
        password_hash = self.hash_password(password)
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id FROM users WHERE id = ? AND password_hash = ?
        ''', (user_id, password_hash))
        return cursor.fetchone() is not None

    def change_password(self, user_id, new_password):
        """Cambiar la contraseña de un usuario."""
        password_hash = self.hash_password(new_password)
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE users SET password_hash = ? WHERE id = ?
            ''', (password_hash, user_id))
            return cursor.rowcount > 0

    def cleanup_duplicate_access(self):
        """Limpiar registros duplicados de la tabla user_access."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM user_access 
                WHERE rowid NOT IN (
                    SELECT MIN(rowid)
                    FROM user_access
                    GROUP BY user_id, branch_name, sub_branch_name
                )
            """)
            return cursor.rowcount
