from src.db.database_manager import DatabaseManager

class DBCashBox(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.initialize_tables()

    def initialize_tables(self):
        self.create_table_caja()
        self.create_table_movimientos()

    def create_table_caja(self):
        query = """
            CREATE TABLE IF NOT EXISTS cashbox (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                descripcion TEXT NOT NULL,
                monto REAL NOT NULL,
                tipo TEXT CHECK (tipo IN ('ingreso', 'egreso')),
                metodo_pago TEXT CHECK (metodo_pago IN ('efectivo', 'tarjeta', 'transferencia', 'cheque', 'deposito', 'otro')),
                movimiento_caja INTEGER,
                user_id INTEGER NOT NULL,
                order_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (order_id) REFERENCES work_orders(work_order_id),
                FOREIGN KEY (movimiento_caja) REFERENCES catalogo_movimientos(id)
            );
        """
        self._execute_query(query)

    def create_table_movimientos(self):
        query = """
            CREATE TABLE IF NOT EXISTS catalogo_movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT CHECK (tipo IN ('ingreso', 'egreso')),
                descripcion TEXT
            );
        """
        self._execute_query(query)

    def _validate_payment_method(self, metodo_pago):
        """Validates if the payment method is allowed."""
        valid_methods = ['efectivo', 'tarjeta', 'transferencia', 'cheque', 'deposito', 'otro']
        if metodo_pago.lower() not in valid_methods:
            raise ValueError(f"Método de pago inválido. Debe ser uno de: {', '.join(valid_methods)}")
        return metodo_pago.lower()

    def create_entry(self, fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id):
        print(fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id)
        try:
            # Validate payment method before insertion
            metodo_pago = self._validate_payment_method(metodo_pago)
            query = """
                INSERT INTO cashbox (fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
            params = (fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id)
            self._execute_query(query, params)
        except ValueError as e:
            raise ValueError(f"Error de validación: {str(e)}")

    def read_entry(self, entry_id):
        query = "SELECT * FROM cashbox WHERE id = ?;"
        params = (entry_id,)
        return self._execute_query(query, params).fetchone()

    def read_all_entries(self):
        query = "SELECT * FROM cashbox;"
        return self._execute_query(query).fetchall()

    def update_entry(self, entry_id, fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id):
        try:
            # Validate payment method
            metodo_pago = self._validate_payment_method(metodo_pago)
            
            # Validate transaction type
            if tipo.lower() not in ['ingreso', 'egreso']:
                raise ValueError("Tipo de transacción inválido. Debe ser 'ingreso' o 'egreso'")
            
            query = """
                UPDATE cashbox
                SET fecha = ?, descripcion = ?, monto = ?, tipo = ?, metodo_pago = ?, user_id = ?, order_id = ?
                WHERE id = ?;
            """
            params = (fecha, descripcion, monto, tipo.lower(), metodo_pago, movimiento_caja, user_id, order_id, entry_id)
            self._execute_query(query, params)
        except ValueError as e:
            raise ValueError(f"Error de validación: {str(e)}")

    def delete_entry(self, entry_id):
        query = "DELETE FROM cashbox WHERE id = ?;"
        params = (entry_id,)
        self._execute_query(query, params)
    
    #Catalogo Movimientos-------------------------------------------------
    def create_movimiento(self, nombre, tipo, descripcion):
        query = """
            INSERT INTO catalogo_movimientos (nombre, tipo, descripcion)
            VALUES (?, ?, ?);
        """
        params = (nombre, tipo, descripcion)
        self._execute_query(query, params)

    def read_movimiento(self, movimiento_id):
        query = "SELECT * FROM catalogo_movimientos WHERE id = ?;"
        params = (movimiento_id,)
        return self._execute_query(query, params).fetchone()

    def read_all_movimientos(self):
        query = "SELECT * FROM catalogo_movimientos;"
        return self._execute_query(query).fetchall()

    def update_movimiento(self, movimiento_id, nombre, tipo, descripcion):
        query = """
            UPDATE catalogo_movimientos
            SET nombre = ?, tipo = ?, descripcion = ?
            WHERE id = ?;
        """
        params = (nombre, tipo, descripcion, movimiento_id)
        self._execute_query(query, params)

    def delete_movimiento(self, movimiento_id):
        query = "DELETE FROM catalogo_movimientos WHERE id = ?;"
        params = (movimiento_id,)
        self._execute_query(query, params)