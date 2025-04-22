class ColaboratorService:
    def __init__(self, db_colaborator):

        self.db_colaborator = db_colaborator

    def create_colaborator(self, nombre, apellido, telefono_personal, documento_identidad,
                           fecha_ingreso, nombre_contacto_emergencia, telefono_emergencia,
                           fecha_baja,salario, is_active, puesto, fecha_nacimiento, numero_seguro_social,
                           informacion_adicional=""):
        """Crear un nuevo colaborador."""
        self.db_colaborator.create_colaborator(nombre, apellido, telefono_personal, documento_identidad,
                           fecha_ingreso, nombre_contacto_emergencia, telefono_emergencia,
                           fecha_baja,salario, is_active, puesto, fecha_nacimiento, numero_seguro_social,
                           informacion_adicional)

    def get_all_colaborators(self):
        """Obtener todos los colaboradores."""
        return self.db_colaborator.get_all_colaborators()

    def get_colaborator_by_id(self, colaborator_id):
        """Obtener un colaborador por su ID."""
        return self.db_colaborator.get_colaborator_by_id(colaborator_id)

    def remove_colaborator_by_id(self, colaborator_id):
        """Eliminar un colaborador por su ID."""
        return self.db_colaborator.remove_colaborator_by_id(colaborator_id)

    def update_colaborator_by_id(self, colaborator_id, **kwargs):
        """Actualizar un colaborador por su ID."""
        success = self.db_colaborator.update_colaborator_by_id(colaborator_id, **kwargs)
        return success

    def create_colaborator_record(self, colaborador_id, fecha, descripcion):
        """Crear un nuevo registro para un colaborador."""
        self.db_colaborator.create_colaborator_record(colaborador_id, fecha, descripcion)

    def get_all_registers(self, colaborador_id):
        """Obtener todos los registros de un colaborador."""
        return self.db_colaborator.get_all_registers(colaborador_id)

    def remove_register(self, register_id):
        """Eliminar un registro por su ID."""
        return self.db_colaborator.remove_register(register_id)
