from PyQt6.QtCore import pyqtSignal, QObject
from src.db.db_operations.db_user import DatabaseUser

class AuthService(QObject):
    user_authenticated = pyqtSignal(dict)

    def __init__(self, db_manager: DatabaseUser):
        super().__init__()
        self.db_manager = db_manager
        self.current_user = None

    def authenticate(self, username, password):
        """
        Autentica un usuario.
        Retorna los datos del usuario si la autenticación es exitosa, None en caso contrario.
        """
        user_data = self.db_manager.get_user(username, password)
        if user_data:
            user_dict = {
                "id": user_data[0],
                "username": user_data[1],
                "role": user_data[2]
            }
            self.current_user = user_dict
            self.user_authenticated.emit(user_dict)
            return user_dict
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
