from src.db.database_manager import DatabaseManager

class DBCashBox(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.initialize_tables()

    def initialize_tables(self):
        self.create_table_caja()
        self.create_table_movimientos()
        self.create_cash_count_denominations_table()
        self.create_index_identifier_table()

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
            index_identifier INTEGER,
            fecha DATE NOT NULL,
            nio_denominations TEXT CHECK (nio_denominations IN ('0.01', '0.05', '0.1', '0.25', '0.5', '1', '5', '10', '20', '50', '100', '200', '500', '1000')),
            us_denominations TEXT CHECK (us_denominations IN ('1', '5', '10', '20', '50', '100')),
            exchange_rate REAL,
            count INTEGER,
            subtotal REAL,
            FOREIGN KEY (id_user_cashier) REFERENCES users(id)
            FOREIGN KEY (index_identifier) REFERENCES index_identifier(id)
        )
        """
        self._execute_query(query)
    
    def create_index_identifier_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS index_identifier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            identifier INTEGER NOT NULL
        );
        """
        self._execute_query(query)

    #Registro de ingreso-------------------------------------------------
    def create_cashbox_entry(self):
        query = """
            INSERT INTO cashbox (fecha, descripcion, monto, tipo, metodo_pago, movimiento_caja, user_id, order_id)
            VALUES (?,?,?,?,?,?,?,?);
        """
        params = (self.fecha, self.descripcion, self.monto, self.tipo, self.metodo_pago, self.movimiento_caja, self.user_id, self.order_id)
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
        index_identifier,
        fecha,
        nio_denominations=None, 
        us_denominations=None, 
        exchange_rate=None, 
        count=0, 
        subtotal=0
        ):
        query = """
        INSERT INTO cash_count_denominations (
            id_user_cashier, 
            index_identifier,
            fecha,
            nio_denominations, 
            us_denominations, 
            exchange_rate, 
            count, 
            subtotal
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (id_user_cashier, index_identifier, fecha, nio_denominations, us_denominations, exchange_rate, count, subtotal)
        self._execute_query(query, params)

    def read_cash_count_denomination(self, user_id):
        query = "SELECT * FROM cash_count_denominations WHERE id_user_cashier = ?"
        cursor = self._execute_query(query, (user_id,))
        return cursor.fetchone()
    
    def get_cash_count_denomination_by_index_identifier(self, index_identifier):
        query = "SELECT * FROM cash_count_denominations WHERE index_identifier =?"
        cursor = self._execute_query(query, (index_identifier,))
        return cursor.fetchall()

    # Indice Identificador-------------------------------------------------
    def get_all_index_identifiers(self):
        query = "SELECT * FROM index_identifier ORDER BY id DESC"
        return self._execute_query(query).fetchall()

    def create_index_identifier(self, identifier, fecha):
        try:
            query = "INSERT INTO index_identifier (identifier, fecha) VALUES (?, ?)"
            self._execute_query(query, (identifier, fecha))
            self.conn.commit()  # Add commit to ensure the transaction is saved
        except Exception as e:
            print(f"Error creating index identifier: {e}")
            raise e

    def get_last_index_identifier(self):
        try:
            query = "SELECT identifier FROM index_identifier ORDER BY id DESC LIMIT 1"
            cursor = self._execute_query(query)
            result = cursor.fetchone()
            return result[0] if result else None  # Return None instead of hardcoded value
        except Exception as e:
            print(f"Error getting last index: {e}")
            return None

    def generate_next_index_identifier(self, fecha):
        try:
            last_identifier = self.get_last_index_identifier()
            new_identifier = 100000001 if last_identifier is None else last_identifier + 1
            self.create_index_identifier(new_identifier, fecha)
            return new_identifier
        except Exception as e:
            print(f"Error generating next index: {e}")
            raise e

    def get_cash_count_by_date_and_index(self, fecha=None, index_identifier=None):
        """Get cash count records by date and/or index identifier"""
        query = """
        SELECT 
            ccd.id,
            ccd.fecha,
            ccd.index_identifier,
            ccd.nio_denominations,
            ccd.us_denominations,
            ccd.exchange_rate,
            ccd.count,
            ccd.subtotal,
            u.username
        FROM cash_count_denominations ccd
        LEFT JOIN users u ON ccd.id_user_cashier = u.id
        WHERE 1=1
        """
        params = []
        
        if fecha:
            query += " AND ccd.fecha = ?"
            params.append(fecha.toString("dd-MM-yyyy"))
        if index_identifier:
            query += " AND ccd.index_identifier = ?"
            params.append(index_identifier)
            
        query += " ORDER BY ccd.fecha DESC, ccd.index_identifier"
        
        try:
            results = self._execute_query(query, tuple(params)).fetchall()
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return [] # return empty list in case of error.

            