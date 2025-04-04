from PyQt6.QtCore import pyqtSignal, QObject
from src.db.db_operations.db_client import DatabaseClient

class ClientService(QObject):
    client_created = pyqtSignal(dict)
    client_updated = pyqtSignal(dict)
    client_removed = pyqtSignal(int)

    def __init__(self, db_manager: DatabaseClient):
        super().__init__()
        self.db_manager = db_manager

    def create_client(self, name, contact_1, contact_2, email, numero_ruc, nombre_empresa):
        """Crear un nuevo cliente y emitir una señal si es exitoso."""
        if self.db_manager.create_client(name, contact_1, contact_2, email, numero_ruc, nombre_empresa):
            client_data = {
                "name": name,
                "contact_1": contact_1,
                "contact_2": contact_2,
                "email": email,
                "numero_ruc": numero_ruc,
                "nombre_empresa": nombre_empresa
            }
            self.client_created.emit(client_data)
            return True
        return False

    def get_all_clients(self):
        """Obtener todos los clientes de la base de datos."""
        clients_data = self.db_manager.get_all_clients()
        if clients_data:
            return [{
                "id": client[0],
                "name": client[1],
                "contact_1": client[2],
                "contact_2": client[3],
                "email": client[4],
                "numero_ruc": client[5],
                "nombre_empresa": client[6]
            } for client in clients_data]
        return []

    def get_client(self, email):
        """Obtener los datos del cliente por correo electrónico."""
        client_data = self.db_manager.get_client(email)
        if client_data:
            return {
                "id": client_data[0],
                "name": client_data[1],
                "contact_1": client_data[2],
                "contact_2": client_data[3],
                "email": client_data[4],
                "numero_ruc": client_data[5],
                "nombre_empresa": client_data[6]
            }
        return None

    def get_client_by_id(self, client_id):
        """Obtener los datos del cliente por ID."""
        client_data = self.db_manager.get_client_by_id(client_id)
        if client_data:
            return {
                "id": client_data[0],
                "name": client_data[1],
                "contact_1": client_data[2],
                "contact_2": client_data[3],
                "email": client_data[4],
                "numero_ruc": client_data[5],
                "nombre_empresa": client_data[6]
            }
        return None

    def update_client_by_id(self, client_id, name=None, contact_1=None, contact_2=None, email=None, numero_ruc=None, nombre_empresa=None):
        """Actualizar los datos de un cliente por ID y emitir una señal si es exitoso."""
        if self.db_manager.update_client_by_id(client_id, name, contact_1, contact_2, email, numero_ruc, nombre_empresa):
            updated_client_data = self.get_client_by_id(client_id)
            self.client_updated.emit(updated_client_data)
            return True
        return False

    def remove_client(self, client_id):
        """Eliminar un cliente por ID y emitir una señal si es exitoso."""
        if self.db_manager.remove_client(client_id):
            self.client_removed.emit(client_id)
            return True
        return False

    def update_client(self, email, name=None, contact_1=None, contact_2=None, numero_ruc=None, nombre_empresa=None):
        """Actualizar los datos de un cliente por correo electrónico y emitir una señal si es exitoso."""
        if self.db_manager.update_client(email, name, contact_1, contact_2, numero_ruc, nombre_empresa):
            updated_client_data = self.get_client(email)
            self.client_updated.emit(updated_client_data)
            return True
        return False
