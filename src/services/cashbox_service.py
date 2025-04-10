class CashBoxService:
    def __init__(self, db_cashbox):
        self.db = db_cashbox

    def create_cashbox_entry_service(self, fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id):
        """Crea un nuevo registro de caja."""
        try:
            return self.db.create_cashbox_entry(
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
            print(f"Error al crear registro de caja: {e}")

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

    def get_cash_count_denomination_by_index_identifier_service(self, index_identifier):
        """Gets a denomination record by index identifier."""
        try:
            return self.db.get_cash_count_denomination_by_index_identifier(index_identifier)
        except Exception as e:
            print(f"Error al obtener denominación por índice identificador: {e}")
    
    # Indice Identificador
    def get_all_index_identifiers_service(self):
        """Gets all index identifiers."""
        try:
            return self.db.get_all_index_identifiers()
        except Exception as e:
            print(f"Error al obtener índices identificadores: {e}")
    
    def create_index_identifier_service(self, id_user_cashier):
        """Creates a new index identifier record."""
        try:
            return self.db.create_index_identifier(id_user_cashier)
        except Exception as e:
            print(f"Error al crear índice identificador: {e}")
    
    def get_last_index_identifier_service(self):
        """Gets the last index identifier."""
        try:
            last_id = self.db.get_last_index_identifier()
            return last_id if last_id is not None else 100000001
        except Exception as e:
            print(f"Error getting last index identifier: {e}")
            return 100000001

    def generate_next_index_identifier_service(self, date):
        """Generates the next index identifier."""
        try:
            return self.db.generate_next_index_identifier(date)
        except Exception as e:
            print(f"Error generating next index identifier: {e}")
            raise e

    def get_cash_count_report_service(self, fecha=None, index_identifier=None):
        """Get cash count report by date and index identifier."""
        try:
            return self.db.get_cash_count_by_date_and_index(fecha, index_identifier)
        except Exception as e:
            print(f"Error al obtener reporte de conteo: {e}")

    #Reportes
    def cashbox_filter_and_totalize_service(self, fecha_inicio, fecha_fin):
        """Filtra y totaliza los registros de caja por fecha."""
        try:
            return self.db.cashbox_filter_and_totalize(fecha_inicio, fecha_fin)
        except Exception as e:
            print(f"Error al filtrar y totalizar registros de caja: {e}")        

    def cashbox_filter_and_totalize_per_movement_service(self, fecha_inicio, fecha_fin):
        """Filtra y totaliza los registros de caja por fecha y movimiento."""
        try:
            return self.db.cashbox_filter_and_totalize_per_movement(fecha_inicio, fecha_fin)
        except Exception as e:
            print(f"Error al filtrar y totalizar registros de caja por movimiento: {e}")

    def cashbox_filter_and_totalize_per_efectivo_service(self, start_date, end_date):
        return self.db.cashbox_filter_and_totalize_per_efectivo(start_date, end_date)

    # Descuentos
    def create_discount_service(self, date, user_id, order_id, discount_mont, discount_percentage, description):
        """Crea un nuevo descuento."""
        try:
            return self.db.create_discount(date, user_id, order_id, discount_mont, discount_percentage, description)
        except Exception as e:
            print(f"Error al crear descuento: {e}")
    
    def get_all_discounts_service(self):
        """Obtiene todos los descuentos."""
        try:
            return self.db.get_all_discounts()
        except Exception as e:
            print(f"Error al obtener descuentos: {e}")
    
    def get_discounts_in_date_range(self, start_date, end_date):
        """Obtiene los descuentos dentro de un rango de fechas."""
        try:
            return self.db.get_discounts_in_date_range(start_date, end_date)
        except Exception as e:
            print(f"Error al obtener descuentos en rango de fechas: {e}")

