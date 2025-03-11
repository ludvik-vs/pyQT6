import sqlite3
from src.db.database_manager import DatabaseManager

class DatabaseProductionOrders(DatabaseManager):
    def __init__(self):
        super().__init__()
