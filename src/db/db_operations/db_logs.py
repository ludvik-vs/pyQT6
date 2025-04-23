from src.db.database_manager import DatabaseManager
import json

class DBLogs(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.initialize_tables()
    
    def initialize_tables(self):
        self.create_table_register_logs()
    
    def create_table_register_logs(self):
        query = """
        CREATE TABLE IF NOT EXISTS register_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            username TEXT NOT NULL,
            activity TEXT NOT NULL
        );
        """
        self._execute_query(query)

    def insert_register_log(self, username, activity):
        query = "INSERT INTO register_logs (username, activity) VALUES (?, ?);"
        self._execute_query(query, (username, activity))

    def get_register_logs_date_range(self, start_date, end_date):
        query = f"SELECT * FROM register_logs WHERE datetime BETWEEN '{start_date}' AND '{end_date}' ORDER BY datetime DESC;"
        result = self._execute_query(query)
        return result

    def get_register_logs_by_user(self, username=None):
        query = "SELECT * FROM register_logs"
        if username:
            query += f" WHERE username = '{username}'"
        query += " ORDER BY datetime DESC;"
        result = self._execute_query(query)
        return result

    def get_register_logs_date_range_json(self, start_date, end_date):
        logs = self.get_register_logs_date_range(start_date, end_date)
        logs_json = []
        for log in logs:
            log_dict = {
                "id": log[0],
                "username": log[2],     # username is in position 2
                "activity": log[3],     # activity is in position 3
                "timestamp": log[1]     # datetime is in position 1, already a string
            }
            logs_json.append(log_dict)
        return json.dumps(logs_json)

    def get_register_logs_json(self, username=None):
        logs = self.get_register_logs_by_user(username)
        logs_json = []
        for log in logs:
            log_dict = {
                "id": log[0],
                "username": log[2],     # username is in position 2
                "activity": log[3],     # activity is in position 3
                "timestamp": log[1]     # datetime is in position 1, already a string
            }
            logs_json.append(log_dict)
        return json.dumps(logs_json)
    