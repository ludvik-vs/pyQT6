from src.db.database_manager import DatabaseManager

class DBCashBox(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.initialize_tables()

    def initialize_tables(self):
        self.create_table_caja()
        self.create_table_movimientos()
        self.create_cash_count_table()
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

    def create_cash_count_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS cash_count (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            register_date DATE NOT NULL,
            operation_type TEXT CHECK (operation_type IN ('apertura', 'cierre')),
            id_cajero INTEGER,
            id_caja INTEGER,
            initial_cash REAL,
            final_cash REAL,
            expected_cash REAL,
            cash_difference REAL,
            remarks TEXT,
            FOREIGN KEY (id_cajero) REFERENCES users(id)
        )
        """
        self._execute_query(query)
    
    def create_cash_count_denominations_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS cash_count_denominations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cash_count INTEGER,
            denominations TEXT CHECK (denominations IN ('0.01', '0.05', '0.1', '0.25', '0.5', '1', '5', '10', '20', '50', '100', '200', '500', '1000')),
            count INTEGER,
            subtotal REAL,
            FOREIGN KEY (id_cash_count) REFERENCES cash_count(id)
        )
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
    
    #Arqueo de Caja-------------------------------------------------
    def create_cash_count(self, register_date, operation_type, id_cajero, id_caja, initial_cash, final_cash, expected_cash, cash_difference, remarks):
        query = """
        INSERT INTO cash_count (register_date, operation_type, id_cajero, id_caja, initial_cash, final_cash, expected_cash, cash_difference, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (register_date, operation_type, id_cajero, id_caja, initial_cash, final_cash, expected_cash, cash_difference, remarks)
        self._execute_query(query, params)

    def read_cash_count(self, cash_count_id):
        query = "SELECT * FROM cash_count WHERE id = ?"
        cursor = self._execute_query(query, (cash_count_id,))
        return cursor.fetchone()

    def update_cash_count(self, cash_count_id, register_date, operation_type, id_cajero, id_caja, initial_cash, final_cash, expected_cash, cash_difference, remarks):
        query = """
        UPDATE cash_count
        SET register_date = ?, operation_type = ?, id_cajero = ?, id_caja = ?, initial_cash = ?, final_cash = ?, expected_cash = ?, cash_difference = ?, remarks = ?
        WHERE id = ?
        """
        params = (register_date, operation_type, id_cajero, id_caja, initial_cash, final_cash, expected_cash, cash_difference, remarks, cash_count_id)
        self._execute_query(query, params)

    def delete_cash_count(self, cash_count_id):
        query = "DELETE FROM cash_count WHERE id = ?"
        self._execute_query(query, (cash_count_id,))
    
    #Arqueo de Efectivo-------------------------------------------------
    def create_cash_count_denomination(self, id_cash_count, denominations, count, subtotal):
        query = """
        INSERT INTO cash_count_denominations (id_cash_count, denominations, count, subtotal)
        VALUES (?, ?, ?, ?)
        """
        params = (id_cash_count, denominations, count, subtotal)
        self._execute_query(query, params)

    def read_cash_count_denomination(self, denomination_id):
        query = "SELECT * FROM cash_count_denominations WHERE id = ?"
        cursor = self._execute_query(query, (denomination_id,))
        return cursor.fetchone()

    def update_cash_count_denomination(self, denomination_id, id_cash_count, denominations, count, subtotal):
        query = """
        UPDATE cash_count_denominations
        SET id_cash_count = ?, denominations = ?, count = ?, subtotal = ?
        WHERE id = ?
        """
        params = (id_cash_count, denominations, count, subtotal, denomination_id)
        self._execute_query(query, params)

    def delete_cash_count_denomination(self, denomination_id):
        query = "DELETE FROM cash_count_denominations WHERE id = ?"
        self._execute_query(query, (denomination_id,))

    def get_daily_totals(self, fecha):
        """
        Get total income and expenses for a specific date
        Args:
            fecha: Date to calculate totals
        Returns:
            dict: Dictionary with date, total income and total expenses
        """
        query = """
            SELECT 
                fecha,
                SUM(CASE WHEN tipo = 'ingreso' THEN monto ELSE 0 END) as total_ingresos,
                SUM(CASE WHEN tipo = 'egreso' THEN monto ELSE 0 END) as total_egresos
            FROM cashbox 
            WHERE fecha = ?
            GROUP BY fecha;
        """
        cursor = self._execute_query(query, (fecha,))
        result = cursor.fetchone()

        if result:
            return {
                "fecha": result[0],
                "total_ingresos": float(result[1] or 0),
                "total_egresos": float(result[2] or 0)
            }
        else:
            return {
                "fecha": fecha,
                "total_ingresos": 0.0,
                "total_egresos": 0.0
            }

    def get_last_cash_count_id(self):
            query = """
            SELECT id FROM cash_count 
            ORDER BY id DESC 
            LIMIT 1;
            """
            cursor = self._execute_query(query)
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_movement_totals(self, fecha):
            """Get totals grouped by movement type"""
            query = """
                SELECT 
                    cm.nombre,
                    cm.tipo,
                    SUM(c.monto) as total
                FROM cashbox c
                JOIN catalogo_movimientos cm ON c.movimiento_caja = cm.id
                WHERE c.fecha = ?
                GROUP BY cm.id, cm.nombre, cm.tipo
                ORDER BY cm.tipo, cm.nombre
            """
            cursor = self._execute_query(query, (fecha,))
            return cursor.fetchall()
    
    def get_payment_method_totals(self, fecha):
            """Get totals grouped by payment method"""
            query = """
                SELECT 
                    metodo_pago,
                    tipo,
                    SUM(monto) as total
                FROM cashbox
                WHERE fecha = ?
                GROUP BY metodo_pago, tipo
                ORDER BY metodo_pago, tipo
            """
            cursor = self._execute_query(query, (fecha,))
            return cursor.fetchall()