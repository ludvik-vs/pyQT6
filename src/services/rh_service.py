from src.db.db_operations.db_colaborator import DatabaseColaborators

class ColaboratorService:
    def __init__(self):
        self.db = DatabaseColaborators()

    def create_colaborator(self, nombre, apellido, telefono_personal, documento_identidad,
                           fecha_ingreso, nombre_contacto_emergencia, telefono_emergencia,
                           fecha_baja,salario, is_active, puesto, fecha_nacimiento, numero_seguro_social,
                           informacion_adicional=""):
        """Crear un nuevo colaborador."""
        self.db.create_colaborator(nombre, apellido, telefono_personal, documento_identidad,
                           fecha_ingreso, nombre_contacto_emergencia, telefono_emergencia,
                           fecha_baja,salario, is_active, puesto, fecha_nacimiento, numero_seguro_social,
                           informacion_adicional)

    def get_all_colaborators(self):
        """Obtener todos los colaboradores."""
        return self.db.get_all_colaborators()

    def get_colaborator_by_id(self, colaborator_id):
        """Obtener un colaborador por su ID."""
        return self.db.get_colaborator_by_id(colaborator_id)

    def remove_colaborator_by_id(self, colaborator_id):
        """Eliminar un colaborador por su ID."""
        return self.db.remove_colaborator_by_id(colaborator_id)

    def update_colaborator_by_id(self, colaborator_id, **kwargs):
        """Actualizar un colaborador por su ID."""
        print(f"Actualizando colaborador con ID: {colaborator_id}")  # Depuración
        success = self.db.update_colaborator_by_id(colaborator_id, **kwargs)
        print(f"Resultado de la actualización: {success}")  # Depuración
        return success
