from src.db.db_operations.db_logs import DBLogs
from datetime import datetime

class LogsServices:
    def __init__(self, db_logs: DBLogs):
        self.db_logs = db_logs

    def register_activity(self, username: str, activity: str) -> None:
        """
        Register a new activity log for a user
        """
        self.db_logs.insert_register_log(username, activity)

    def get_logs_by_date_range(self, start_date: str, end_date: str) -> list:
        """
        Get logs within a date range
        """
        return self.db_logs.get_register_logs_date_range(start_date, end_date)

    def get_logs_by_user(self, username: str = None) -> list:
        """
        Get logs for a specific user or all users if username is None
        """
        return self.db_logs.get_register_logs_by_user(username)

    def get_logs_by_date_range_json(self, start_date: str, end_date: str) -> str:
        """
        Get logs within a date range in JSON format
        """
        return self.db_logs.get_register_logs_date_range_json(start_date, end_date)

    def get_logs_json(self, username: str = None) -> str:
        """
        Get logs for a specific user or all users in JSON format
        """
        return self.db_logs.get_register_logs_json(username)

    def validate_date_format(self, date_str: str) -> bool:
        """
        Validate if a date string has the correct format (YYYY-MM-DD HH:MM:SS)
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False