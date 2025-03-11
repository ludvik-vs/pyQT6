import sqlite3
from src.db.database_manager import DatabaseManager

class DatabaseWorkOrders(DatabaseManager):
    def __init__(self):
        super().__init__()
