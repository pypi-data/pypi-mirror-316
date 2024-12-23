import os
import sqlite3
import importlib


class DatabaseConfig:
    _database_name = None

    @classmethod
    def get_database(cls):
        settings_module = None
        if cls._database_name is None:
            try:
                settings_module = os.environ.get("SQLORM_SETTINGS_MODULE", "settings")
                settings = importlib.import_module(settings_module)
                cls._database_name = getattr(settings, "DATABASE_NAME", None)
                if not cls._database_name:
                    raise ValueError("DATABASE_NAME is not set in the specified settings module.")
            except ModuleNotFoundError:
                raise ValueError(f"Settings module '{settings_module}' not found. Please create the file.")
        return cls._database_name


# def connect_to_database():
#     """
#     Establish a connection to the database.
#     """
#     if not DATABASE_NAME:
#         raise ValueError("DATABASE_NAME is not set in settings.py.")
#     return sqlite3.connect(DATABASE_NAME)

def connect_to_database():
    """
    Establish a connection to the database.
    """
    db_name = DatabaseConfig.get_database()
    return sqlite3.connect(db_name)
