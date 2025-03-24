class CashBoxService:
    def __init__(self, db_cashbox):
        self.db = db_cashbox

    def read_cashbox_entry_service(self, entry_id):
        try:
            return self.db.read_entry(entry_id)
        except Exception as e:
            print(f"Error al leer registro de caja: {e}")
    
    def read_all_entries_service(self):
        try:
            return self.db.read_all_entries()
        except Exception as e:
            print(f"Error al leer registros de caja: {e}")

    def update_entry_service(self, entry_id, fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id):
        """Actualiza un registro de caja existente."""
        try:
            return self.db.update_entry(
                entry_id=entry_id,
                fecha=fecha,
                descripcion=descripcion,
                monto=monto,
                tipo=tipo,
                metodo_pago=metodo_pago,
                movimiento_caja=movimiento_caja,
                user_id=user_id,
                order_id=order_id
            )
        except Exception as e:
            print(f"Error al actualizar registro de caja: {e}")
    
    def delete_entry_service(self, entry_id):
        """Elimina un registro de caja existente."""
        try:
            return self.db.delete_entry(entry_id)
        except Exception as e:
            print(f"Error al eliminar registro de caja: {e}")
    
    # Catalogo Movimientos

    def create_movimiento_service(self, nombre, tipo, descripcion):
        """Crea un nuevo movimiento en el catálogo de movimientos."""
        try:
            return self.db.create_movimiento(nombre, tipo, descripcion)
        except Exception as e:
            print(f"Error al crear movimiento: {e}")

    def read_movimiento_service(self, movimiento_id):
        """Lee un movimiento del catálogo de movimientos."""
        try:
            return self.db.read_movimiento(movimiento_id)
        except Exception as e:
            print(f"Error al leer movimiento: {e}")

    def read_all_movimientos_service(self):
        """Lee todos los movimientos del catálogo de movimientos."""
        try:
            return self.db.read_all_movimientos()
        except Exception as e:
            print(f"Error al leer movimientos: {e}")
    
    def update_movimiento_service(self, movimiento_id, nombre, tipo, descripcion):
        """Actualiza un movimiento existente en el catálogo de movimientos."""
        try:
            return self.db.update_movimiento(movimiento_id, nombre, tipo, descripcion)
        except Exception as e:
            print(f"Error al actualizar movimiento: {e}")
    
    def delete_movimiento_service(self, movimiento_id):
        """Elimina un movimiento existente del catálogo de movimientos."""
        try:
            return self.db.delete_movimiento(movimiento_id)
        except Exception as e:
            print(f"Error al eliminar movimiento: {e}")

    # Conteo Efectivo
    def create_cash_count_denomination_service(
        self, 
        id_user_cashier=None, 
        index_identifier=None,
        fecha=None,
        nio_denominations=None, 
        us_denominations=None, 
        exchange_rate=None, 
        count=0, 
        subtotal=0
        ):
        """Creates a new denomination record with support for both NIO and USD."""
        try:
            return self.db.create_cash_count_denomination(
                id_user_cashier, index_identifier, fecha, nio_denominations, us_denominations, exchange_rate, count, subtotal
            )
        except Exception as e:
            print(f"Error al crear denominación: {e}")

    def read_cash_count_denomination_service(self, user_id):
        """Reads a denomination record."""
        try:
            return self.db.read_cash_count_denomination(user_id)
        except Exception as e:
            print(f"Error al leer denominación: {e}")

    # Indice Identificador

    def create_index_identifier_service(self, id_user_cashier):
        """Creates a new index identifier record."""
        try:
            return self.db.create_index_identifier(id_user_cashier)
        except Exception as e:
            print(f"Error al crear índice identificador: {e}")
    
    def get_last_index_identifier_service(self):
        """Gets the last index identifier."""
        try:
            return self.db.get_last_index_identifier()
        except Exception as e:
            print(f"Error al obtener último índice identificador: {e}")

    def generate_next_index_identifier_service(self, date):
        """Generates the next index identifier."""
        try:
            return self.db.generate_next_index_identifier(date)
        except Exception as e:
            print(f"Error al generar siguiente índice identificador: {e}")

    def get_cash_count_report_service(self, fecha=None, index_identifier=None):
        """Get cash count report by date and index identifier."""
        try:
            return self.db.get_cash_count_by_date_and_index(fecha, index_identifier)
        except Exception as e:
            print(f"Error al obtener reporte de conteo: {e}")