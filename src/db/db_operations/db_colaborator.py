import sqlite3
from src.db.database_manager import DatabaseManager

class DatabaseColaborators(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.create_client_table()
        self.insert_default_colaborator()

    def create_client_table(self):
        """Crear la tabla de colaboradores."""
        query_1 = '''
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
        '''
        query_2 = '''
            CREATE TABLE IF NOT EXISTS registros_colaborador (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                colaborador_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                descripcion TEXT NOT NULL,
                FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id)
            )
        '''
        self.create_tables([query_1, query_2])

    def insert_default_colaborator(self):
        """Insertar un colaborador por defecto."""
        default_colaborator = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "telefono_personal": "123-456-7890",
            "documento_identidad": "A12345678",
            "fecha_ingreso": "2023-01-01",
            "nombre_contacto_emergencia": "María Pérez",
            "telefono_emergencia": "098-765-4321",
            "fecha_baja": "",
            "salario": 3000.00,
            "is_active": 1,
            "puesto": "Desarrollador",
            "fecha_nacimiento": "1990-05-15",
            "numero_seguro_social": "SS123456789",
            "informacion_adicional": "Ninguna"
        }
        self.create_colaborator(**default_colaborator)

    def create_colaborator(self, nombre, apellido, telefono_personal, documento_identidad,
                           fecha_ingreso, nombre_contacto_emergencia, telefono_emergencia,
                           fecha_baja,salario, is_active, puesto, fecha_nacimiento, numero_seguro_social,
                           informacion_adicional=""):
        """Crear un nuevo colaborador."""
        query = '''
            INSERT INTO colaboradores (
                nombre, apellido, telefono_personal, documento_identidad,
                fecha_ingreso, nombre_contacto_emergencia, telefono_emergencia,
                fecha_baja,salario, is_active, puesto, fecha_nacimiento, numero_seguro_social,
                informacion_adicional
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, (
            nombre, apellido, telefono_personal, documento_identidad,
            fecha_ingreso, nombre_contacto_emergencia, telefono_emergencia,
            fecha_baja,salario, is_active, puesto, fecha_nacimiento, numero_seguro_social,
            informacion_adicional
        ))

    def get_all_colaborators(self):
        """Obtener todos los colaboradores."""
        query = 'SELECT * FROM colaboradores'
        return self.fetch_all(query)

    def get_colaborator_by_id(self, colaborator_id):
        """Obtener un colaborador por su ID."""
        query = 'SELECT * FROM colaboradores WHERE id = ?'
        return self.fetch_one(query, (colaborator_id,))

    def remove_colaborator_by_id(self, colaborator_id):
        """Eliminar un colaborador por su ID."""
        query = '''DELETE FROM colaboradores WHERE id = ?'''
        try:
            self.execute_query(query, (colaborator_id,))
            print(f"Colaborador con ID {colaborator_id} eliminado exitosamente.")  # Depuración
            return True  # Indicar que la operación fue exitosa
        except Exception as e:
            print(f"Error al eliminar colaborador: {e}")
            return False  # Indicar que hubo un error

    def update_colaborator_by_id(self, colaborator_id, **kwargs):
        """Actualizar un colaborador por su ID."""
        fields = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values())
        values.append(colaborator_id)
        query = f'UPDATE colaboradores SET {fields} WHERE id = ?'
        try:
            self.execute_query(query, values)
            print(f"Consulta ejecutada: {query} con valores {values}")  # Depuración
            return True  # Indicar que la operación fue exitosa
        except Exception as e:
            print(f"Error al actualizar colaborador: {e}")
            return False  # Indicar que hubo un error

    def create_colaborator_record(self, colaborador_id, fecha, descripcion):
        """Crear un nuevo registro para un colaborador."""
        query = '''
            INSERT INTO registros_colaborador (colaborador_id, fecha, descripcion)
            VALUES (?, ?, ?)
        '''
        self.execute_query(query, (colaborador_id, fecha, descripcion))

    def get_all_registers(self, colaborador_id):
        """Obtener todos los registros de un colaborador."""
        query = '''
            SELECT * FROM registros_colaborador WHERE colaborador_id = ? ORDER BY fecha DESC
        '''
        return self.fetch_all(query, (colaborador_id,))

    def remove_register(self, register_id):
        """Eliminar un registro por su ID."""
        query = '''DELETE FROM registros_colaborador WHERE id = ?'''
        try:
            self.execute_query(query, (register_id,))
            print(f"Registro con ID {register_id} eliminado exitosamente.")  # Depuración
            return True  # Indicar que la operación fue exitosa
        except Exception as e:
            print(f"Error al eliminar registro: {e}")
            return False  # Indicar que hubo un error
