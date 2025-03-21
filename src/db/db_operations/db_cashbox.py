from src.db.database_manager import DatabaseManager

class DBCashBox(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.initialize_tables()

    def initialize_tables(self):
        self.create_table_caja()
        self.create_table_movimientos()
        self.create_cash_count_denominations_table()

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

    def create_cash_count_denominations_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS cash_count_denominations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user_cashier INTEGER,
            nio_denominations TEXT CHECK (nio_denominations IN ('0.01', '0.05', '0.1', '0.25', '0.5', '1', '5', '10', '20', '50', '100', '200', '500', '1000')),
            us_denominations TEXT CHECK (us_denominations IN ('1', '5', '10', '20', '50', '100')),
            exchange_rate REAL,
            count INTEGER,
            subtotal REAL,
            FOREIGN KEY (id_user_cashier) REFERENCES users(id)
        )
        """
        self._execute_query(query)
    
    #Arqueo de Efectivo-------------------------------------------------
    def save_denomination_count(self, fecha, currency_type, denomination, count, subtotal, exchange_rate=None):
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
        if currency_type.lower() == 'nio':
            query = """
            INSERT INTO cash_count_denominations (nio_denominations, count, subtotal)
            VALUES (?, ?, ?)
            """
            params = (denomination, count, subtotal)
        else:
            query = """
            INSERT INTO cash_count_denominations (us_denominations, count, subtotal, exchange_rate)
            VALUES (?, ?, ?, ?)
            """
            params = (denomination, count, subtotal, exchange_rate)
            
        self._execute_query(query, params)
        
    def get_denominations_by_date(self, fecha):
        """
        Get all denominations for a specific date
        """
        query = """
        SELECT cd.id, cd.nio_denominations, cd.us_denominations, cd.exchange_rate, cd.count, cd.subtotal
        FROM cash_count_denominations cd
        JOIN cash_count cc ON cd.id_cash_count = cc.id
        WHERE cc.register_date = ?
        """
        cursor = self._execute_query(query, (fecha,))
        return cursor.fetchall()

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
    
    #Arqueo de Efectivo-------------------------------------------------
    def create_cash_count_denomination(
        self, 
        id_user_cashier, 
        nio_denominations=None, 
        us_denominations=None, 
        exchange_rate=None, 
        count=0, 
        subtotal=0
        ):
        query = """
        INSERT INTO cash_count_denominations (
            id_user_cashier, 
            nio_denominations, 
            us_denominations, 
            exchange_rate, 
            count, 
            subtotal
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (id_user_cashier, nio_denominations, us_denominations, exchange_rate, count, subtotal)
        self._execute_query(query, params)

    def read_cash_count_denomination(self, user_id):
        query = "SELECT * FROM cash_count_denominations WHERE id_user_cashier = ?"
        cursor = self._execute_query(query, (user_id,))
        return cursor.fetchone()
