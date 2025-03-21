class CashBoxService:
    def __init__(self, db_cashbox):
        self.db = db_cashbox

    def create_cashbox_entry_service(self, fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id):
        try:
            return self.db.create_entry(fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id)
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

    # Cash Count Services -------------------------------------------------
    def create_cash_count_service(self, register_date, operation_type, id_cajero, id_caja, initial_cash, final_cash, expected_cash, cash_difference, remarks):
        """Creates a new cash count record."""
        try:
            return self.db.create_cash_count(
                register_date, operation_type, id_cajero, id_caja,
                initial_cash, final_cash, expected_cash, cash_difference, remarks
            )
        except Exception as e:
            print(f"Error al crear arqueo de caja: {e}")

    def read_cash_count_service(self, cash_count_id):
        """Reads a cash count record."""
        try:
            return self.db.read_cash_count(cash_count_id)
        except Exception as e:
            print(f"Error al leer arqueo de caja: {e}")

    def update_cash_count_service(self, cash_count_id, register_date, operation_type, id_cajero, id_caja, initial_cash, final_cash, expected_cash, cash_difference, remarks):
        """Updates an existing cash count record."""
        try:
            return self.db.update_cash_count(
                cash_count_id, register_date, operation_type, id_cajero, id_caja,
                initial_cash, final_cash, expected_cash, cash_difference, remarks
            )
        except Exception as e:
            print(f"Error al actualizar arqueo de caja: {e}")

    def delete_cash_count_service(self, cash_count_id):
        """Deletes a cash count record."""
        try:
            return self.db.delete_cash_count(cash_count_id)
        except Exception as e:
            print(f"Error al eliminar arqueo de caja: {e}")

    # Cash Count Denominations Services -------------------------------------------------
    def create_cash_count_denomination_service(
        self, 
        id_cash_count=None, 
        id_user_cashier=None, 
        nio_denominations=None, 
        us_denominations=None, 
        exchange_rate=None, 
        count=0, 
        subtotal=0
        ):
        """Creates a new denomination record with support for both NIO and USD."""
        try:
            return self.db.create_cash_count_denomination(
                id_cash_count, id_user_cashier, nio_denominations, us_denominations, exchange_rate, count, subtotal
            )
        except Exception as e:
            print(f"Error al crear denominación: {e}")

    def read_cash_count_denomination_service(self, denomination_id):
        """Reads a denomination record."""
        try:
            return self.db.read_cash_count_denomination(denomination_id)
        except Exception as e:
            print(f"Error al leer denominación: {e}")
    
    def read_cash_count_denominations_by_cash_count_id_service(self, id_cash_count):
        """Get all denominations for a specific cash count"""
        try:
            return self.db.read_cash_count_denominations_by_cash_count_id(id_cash_count)
        except Exception as e:
            print(f"Error al leer denominaciones por arqueo: {e}")
            return []

    def update_cash_count_denomination_service(self, denomination_id, id_cash_count=None, nio_denominations=None, us_denominations=None, exchange_rate=None, count=0, subtotal=0):
        """Updates an existing denomination record with support for both NIO and USD."""
        try:
            return self.db.update_cash_count_denomination(
                denomination_id, id_cash_count, nio_denominations, us_denominations, exchange_rate, count, subtotal
            )
        except Exception as e:
            print(f"Error al actualizar denominación: {e}")

    def delete_cash_count_denomination_service(self, denomination_id):
        """Deletes a denomination record."""
        try:
            return self.db.delete_cash_count_denomination(denomination_id)
        except Exception as e:
            print(f"Error al eliminar denominación: {e}")
    
    def save_denomination_count_service(self, fecha, currency_type, denomination, count, subtotal, exchange_rate=None):
        """
        Save denomination count without requiring a cash_count_id
        Args:
            fecha: Date of the count
            currency_type: 'nio' or 'usd'
            denomination: Denomination value
            count: Number of bills/coins
            subtotal: Total value
            exchange_rate: Exchange rate for USD (only needed for USD)
        """
        try:
            return self.db.save_denomination_count(fecha, currency_type, denomination, count, subtotal, exchange_rate)
        except Exception as e:
            print(f"Error al guardar conteo de denominación: {e}")
    
    def get_denominations_by_date_service(self, fecha):
        """Get all denominations for a specific date"""
        try:
            return self.db.get_denominations_by_date(fecha)
        except Exception as e:
            print(f"Error al obtener denominaciones por fecha: {e}")
            return []

    def get_daily_totals_service(self, fecha):
        """
        Get total income and expenses for a specific date through service layer
        Args:
            fecha: Date to calculate totals
        Returns:
            dict: Dictionary with date, total income and total expenses
        """
        try:
            return self.db.get_daily_totals(fecha)
        except Exception as e:
            print(f"Error al obtener totales diarios: {e}")
            return {
                "fecha": fecha,
                "total_ingresos": 0.0,
                "total_egresos": 0.0
            }

    def get_last_cash_count_id_service(self):
        try:
            return self.db.get_last_cash_count_id()
        except Exception as e:
            print(f"Error al obtener último ID de arqueo: {e}")

    def get_movement_totals_service(self, fecha):
        """Get totals by movement type"""
        try:
            return self.db.get_movement_totals(fecha)
        except Exception as e:
            print(f"Error al obtener totales por movimiento: {e}")
            return []

    def get_payment_method_totals_service(self, fecha):
        """Get totals by payment method"""
        try:
            return self.db.get_payment_method_totals(fecha)
        except Exception as e:
            print(f"Error al obtener totales por método de pago: {e}")
            return []
            

    