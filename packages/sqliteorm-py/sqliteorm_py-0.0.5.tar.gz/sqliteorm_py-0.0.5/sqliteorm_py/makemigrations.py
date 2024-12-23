import sqlite3
import inspect
import importlib
from sqliteorm_py.basemodel import BaseModel
from sqliteorm_py.connect_to_db import connect_to_database


def get_models_from_module(module_name="models"):
    """
    Fetch all models from the specified module.
    """
    try:
        module = importlib.import_module(module_name)
        model_classes = [
            cls for _, cls in inspect.getmembers(module, inspect.isclass)
            if issubclass(cls, BaseModel) and cls is not BaseModel
        ]
        return model_classes
    except ModuleNotFoundError as e:
        print(f"Error importing module '{module_name}': {e}")
        return []


def get_existing_tables():
    """
    Fetches the list of user-defined tables in the database,
    excluding system tables like 'sqlite_sequence'.
    """
    conn = None
    try:
        conn = connect_to_database()  # Trying to establish a connection
        cursor = conn.cursor()

        # Fetch tables from sqlite_master, excluding system tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}

        # Exclude system tables like sqlite_sequence
        protected_tables = {'sqlite_sequence'}
        return tables - protected_tables

    except sqlite3.Error as e:
        print(f"Database error while fetching tables: {e}")
        return set()  # Return an empty set if there's a database error

    except Exception as e:
        print(f"Unexpected error: {e}")
        return set()  # Return an empty set in case of other errors

    finally:
        if conn:
            conn.close()  # Ensure that the connection is always closed


def drop_table(table_name):
    """
    Drop a specific table from the database.
    :param table_name: Name of the table to drop.
    """

    conn = connect_to_database()
    try:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE {table_name}")
        conn.commit()
        print(f"Table '{table_name}' dropped successfully.")
    except sqlite3.Error as e:
        print(f"Error dropping table '{table_name}': {e}")
    finally:
        if conn:
            conn.close()


def drop_removed_tables():
    """
    Drop tables in the database that no longer have corresponding models.
    """
    bool1 = False
    try:
        # Get all models and existing tables
        models = get_models_from_module()
        existing_tables = get_existing_tables()

        # Extract table names from models
        model_tables = {model.table_name or model.__name__.lower() for model in models}

        # Identify tables to drop
        tables_to_drop = existing_tables - model_tables

        # Drop each table using the drop_table function
        for table in tables_to_drop:
            drop_table(table)  # Use the reusable function here
            bool1 = True

    except Exception as e:
        print(f"Error in drop_removed_tables: {e}")

    return bool1


def run_migrations():
    """
    Run the migration process to synchronize models with database tables.
    """

    models = get_models_from_module()
    existing_tables = get_existing_tables()
    migrations_performed = False

    # Handle removed tables
    drop = drop_removed_tables()

    for model in models:
        table_name = model.table_name or model.__name__.lower()

        if table_name not in existing_tables:
            # Create a new table
            print(f"Creating table: {table_name}")
            model.create_table()
            migrations_performed = True
        else:
            # Synchronize existing table
            print(f"Synchronizing table: {table_name}")
            bool1, msg = model.remove_missing_columns()  # Remove fields not in the model
            bool2, msg2 = model.sync_fields()  # Add new fields

            if not bool2 and bool1:
                print(msg)
            elif bool2 and bool1:
                print(msg)
            elif not bool2 and not bool1:
                print(msg2)

            migrations_performed = True

    if not migrations_performed:
        if not drop:
            print("No migrations needed.")
