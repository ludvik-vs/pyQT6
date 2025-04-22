from src.db.db_operations.db_logs import DBLogs
from datetime import datetime

class LogsServices:
    """
    Service class for managing system activity logs.
    
    This class provides an interface for recording and retrieving user activities
    in the system, including login events, operations, and system actions.
    
    Attributes:
        db_logs (DBLogs): Database manager instance for log operations
    """

    def __init__(self, db_logs: DBLogs):
        """
        Initialize the LogsServices with a database manager.
        
        Args:
            db_logs (DBLogs): Instance of DBLogs for database operations
        """
        self.db_logs = db_logs

    def register_activity(self, username: str, activity: str) -> None:
        """
        Register a new activity log for a user.
        
        Args:
            username (str): The username of the user performing the activity
            activity (str): Description of the activity performed
        
        Returns:
            None
        """
        self.db_logs.insert_register_log(username, activity)

    def get_logs_by_date_range(self, start_date: str, end_date: str) -> list:
        """
        Get logs within a specified date range.
        
        Args:
            start_date (str): Start date in format 'YYYY-MM-DD HH:MM:SS'
            end_date (str): End date in format 'YYYY-MM-DD HH:MM:SS'
        
        Returns:
            list: List of log entries within the specified date range
                  Each entry contains: [id, username, activity, timestamp]
        """
        return self.db_logs.get_register_logs_date_range(start_date, end_date)

    def get_logs_by_user(self, username: str = None) -> list:
        """
        Get logs for a specific user or all users.
        
        Args:
            username (str, optional): Username to filter logs. If None, returns all logs
        
        Returns:
            list: List of log entries for the specified user or all users
                  Each entry contains: [id, username, activity, timestamp]
        """
        return self.db_logs.get_register_logs_by_user(username)

    def get_logs_by_date_range_json(self, start_date: str, end_date: str) -> str:
        """
        Get logs within a date range in JSON format.
        
        Args:
            start_date (str): Start date in format 'YYYY-MM-DD HH:MM:SS'
            end_date (str): End date in format 'YYYY-MM-DD HH:MM:SS'
        
        Returns:
            str: JSON string containing log entries with fields:
                 {id, username, activity, timestamp}
        """
        return self.db_logs.get_register_logs_date_range_json(start_date, end_date)

    def get_logs_json(self, username: str = None) -> str:
        """
        Get logs for a specific user or all users in JSON format.
        
        Args:
            username (str, optional): Username to filter logs. If None, returns all logs
        
        Returns:
            str: JSON string containing log entries with fields:
                 {id, username, activity, timestamp}
        """
        return self.db_logs.get_register_logs_json(username)

    def validate_date_format(self, date_str: str) -> bool:
        """
        Validate if a date string has the correct format.
        
        Args:
            date_str (str): Date string to validate in format 'YYYY-MM-DD HH:MM:SS'
        
        Returns:
            bool: True if date string is valid, False otherwise
        
        Example:
            >>> validate_date_format("2023-12-31 23:59:59")
            True
            >>> validate_date_format("2023-13-45")
            False
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False