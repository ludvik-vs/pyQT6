class CashBoxService:
    def __init__(self, db_cashbox):
        self.db = db_cashbox

    def create_cashbox_entry_service(self, fecha, descripcion, monto, tipo, metodo_pago, user_id, order_id):
        try:
            return self.db.create_entry(fecha, descripcion, monto, tipo, metodo_pago, user_id, order_id)
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

    def update_entry_service(self, entry_id, fecha, descripcion, monto, tipo, metodo_pago, user_id, order_id):
        """Actualiza un registro de caja existente."""
        try:
            return self.db.update_entry(
                entry_id=entry_id,
                fecha=fecha,
                descripcion=descripcion,
                monto=monto,
                tipo=tipo,
                metodo_pago=metodo_pago,
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