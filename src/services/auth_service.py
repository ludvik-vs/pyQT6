from PyQt6.QtCore import pyqtSignal, QObject
from src.db.db_operations.db_user import DatabaseUser

class UserData(QObject):
    user_id_changed = pyqtSignal(int)
    username_changed = pyqtSignal(str)
    role_changed = pyqtSignal(str)
    access_changed = pyqtSignal(list)

    def __init__(self, user_id=None, username=None, role=None, access=None):
        super().__init__()
        self._user_id = user_id
        self._username = username
        self._role = role
        self._access = access

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value
        self.user_id_changed.emit(value)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        self.username_changed.emit(value)

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value
        self.role_changed.emit(value)

    @property
    def access(self):
        return self._access

    @access.setter
    def access(self, value):
        self._access = value
        self.access_changed.emit(value)

    def __str__(self):
        return f"User ID: {self.user_id}, Username: {self.username}, Role: {self.role}, Access: {self.access}"

class AuthService(QObject):
    user_authenticated = pyqtSignal(UserData)

    def __init__(self, db_manager: DatabaseUser):
        super().__init__()
        self.db_manager = db_manager
        self.current_user = None

    def authenticate(self, username, password):
        """
        Autentica un usuario.
        Retorna los datos del usuario si la autenticación es exitosa, None en caso contrario.
        """
        print(f"Authenticating user: {username}")
        user_data = self.db_manager.get_user(username, password)
        if user_data:
            user = UserData(
                user_id=user_data[0],
                username=user_data[1],
                role=user_data[2],
                access=self.db_manager.get_user_access(user_data[0])
            )
            self.current_user = user
            self.user_authenticated.emit(user)
            return user
        print("Authentication failed")
        return None

    def get_current_user(self):
        """
        Retorna la información del usuario autenticado.
        Retorna None si no hay usuario autenticado.
        """
        return self.current_user

    def logout(self):
        """
        Cierra la sesión del usuario.
        """
        print("Logging out user")
        self.current_user = None

    def register_user(self, username, password, role='user'):
        """
        Registra un nuevo usuario.
        Retorna True si el registro es exitoso, False si el usuario ya existe.
        """
        return self.db_manager.create_user(username, password, role)

    def delete_user(self, user_id):
        """
        Elimina un usuario por su ID.
        Retorna True si la eliminación es exitosa, False en caso contrario.
        """
        return self.db_manager.remove_user(user_id)

    def update_user(self, user_id, new_username=None, new_password=None, new_role=None):
        """
        Actualiza los datos de un usuario.
        Retorna True si la actualización es exitosa, False en caso contrario.
        """
        if not self.db_manager.conn:
            self.db_manager.connect()
        cursor = self.db_manager.conn.cursor()

        # Construir la consulta SQL dinámicamente basada en los campos proporcionados
        updates = []
        params = []
        if new_username:
            updates.append("username = ?")
            params.append(new_username)
        if new_password:
            updates.append("password_hash = ?")
            params.append(self.db_manager.hash_password(new_password))
        if new_role:
            updates.append("role = ?")
            params.append(new_role)

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"

        with self.db_manager.conn:
            cursor.execute(query, params)
            return cursor.rowcount > 0

    def get_all_users(self):
        """
        Obtener todos los usuarios desde la base de datos.
        """
        return self.db_manager.get_all_users()

    def verify_password(self, user_id, password):
        """
        Verificar la contraseña de un usuario.
        Retorna True si la contraseña es correcta, False en caso contrario.
        """
        return self.db_manager.verify_password(user_id, password)

    def change_password(self, user_id, new_password):
        """
        Cambiar la contraseña de un usuario.
        Retorna True si la actualización es exitosa, False en caso contrario.
        """
        return self.db_manager.change_password(user_id, new_password)
