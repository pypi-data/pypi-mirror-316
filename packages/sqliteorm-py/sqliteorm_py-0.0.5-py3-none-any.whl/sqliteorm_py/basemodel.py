import sqlite3
from sqliteorm_py.connect_to_db import connect_to_database
from sqliteorm_py.fields import Field, ForeignKey, CharField


class QuerySet:
    def __init__(self, model_class, records):
        self.model_class = model_class
        self.records = records

    def delete(self):
        """
        Delete all records in the QuerySet from the database.
        """
        try:
            if not self.records:
                print("No records to delete.")
                return

            # Delete each record
            for record in self.records:
                sql = f"DELETE FROM {self.model_class.table_name} WHERE id = ?"
                self.model_class._execute_sql(sql, (record.id,))
            print(f"{len(self.records)} records deleted from table '{self.model_class.table_name}'.")

        except sqlite3.Error as e:
            print(f"Database error while deleting records: {e}")
        except Exception as e:
            print(f"Unexpected error in delete method: {e}")

    def update(self, **updates):
        """
        Update all records in the QuerySet.
        :param updates: A dictionary of column names and their new values.
        """
        try:
            if not updates:
                print("You must provide at least one field with a value to update.")
                return
            # Step 1: Validate the fields before applying updates
            self.model_class.validate_fields(updates)

            for record in self.records:
                # Apply updates to each record
                for field, value in updates.items():
                    setattr(record, field, value)  # Update each field in the record

                # Generate the SQL UPDATE query
                columns = ", ".join([f"{field} = ?" for field in updates.keys()])
                values = tuple(updates.values()) + (record.id,)  # Including the record's ID for WHERE clause
                sql = f"UPDATE {self.model_class.table_name} SET {columns} WHERE id = ?"

                # Execute the SQL query to update the record in the database
                self.model_class._execute_sql(sql, values)

            print(f"{len(self.records)} records updated in table '{self.model_class.table_name}'.")

        except sqlite3.Error as e:
            print(f"Database error while updating records: {e}")
        except Exception as e:
            print(f"Unexpected error in update method: {e}")

    def __iter__(self):
        """
        Allow iteration over the records.
        """
        return iter(self.records)

    def __len__(self):
        """
        Return the number of records in the QuerySet.
        """
        return len(self.records)

    def __getitem__(self, index):
        """
        Allow indexing of records.
        """
        return self.records[index]

    def __repr__(self):
        """
        Return a string representation of the QuerySet.
        """
        return f"<QuerySet {self.records}>"


class BaseModel:
    table_name = None

    def __init__(self, **kwargs):
        # print(f"kwargs: {kwargs}")
        for name, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                value = kwargs.get(name, None)
                setattr(self, name, value)

    @classmethod
    def validate_fields(cls, kwargs):
        model_fields = {
            name: field for name, field in cls.__dict__.items() if isinstance(field, Field)
        }

        for name, field in model_fields.items():
            if name in kwargs:
                value = kwargs[name]
                if value is None and not field.null:
                    raise ValueError(f"Field '{name}' cannot be NULL.")

                if value == "" and not field.blank:
                    raise ValueError(f"Field '{name}' cannot be blank.")

                if isinstance(field, CharField):
                    max_length = int(field.db_type.split("(")[1].split(")")[0])
                    if len(value) > max_length:
                        raise ValueError(f"Field '{name}' exceeds max_length of {max_length}.")

                if not isinstance(value, field.expected_type):
                    raise TypeError(f"Field '{name}' must be of type {field.expected_type.__name__}.")

    @classmethod
    def _execute_sql(cls, sql, params=None):
        """
        Execute SQL query with parameters and return the number of affected rows.
        Ensures proper connection closure and handles errors gracefully.
        """
        conn = None
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute(sql, params or [])
            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows if affected_rows is not None else 0
        except sqlite3.Error as e:
            print(f"Database error while executing SQL: {e}")
            print(f"SQL: {sql}")
            print(f"Parameters: {params}")
            return 0
        except Exception as e:
            print(f"Unexpected error in _execute_sql method: {e}")
            return 0
        finally:
            if conn:
                conn.close()

    @classmethod
    def create_table(cls):
        """
        Create the table for the model, with error handling for SQL execution.
        """
        try:
            fields = []
            foreign_keys = []
            unique_constraints = []
            for name, field in cls.__dict__.items():
                if isinstance(field, Field):

                    unique_constraint = "UNIQUE" if getattr(field, "unique", False) else ""
                    fields.append(f"{name} {field.db_type} {unique_constraint}")

                    if isinstance(field, ForeignKey):
                        related_table = field.related_model.table_name or field.related_model.__name__.lower()
                        foreign_keys.append(
                            f"FOREIGN KEY ({name}) REFERENCES {related_table}(id) ON DELETE {field.on_delete}"
                        )

            fields_sql = ", ".join(fields + foreign_keys)
            sql = f"CREATE TABLE IF NOT EXISTS {cls.table_name or cls.__name__.lower()} ({fields_sql})"
            cls._execute_sql(sql)
        except Exception as e:
            print(f"Error while creating table '{cls.table_name or cls.__name__.lower()}': {e}")

    @classmethod
    def insert(cls, verbose=True, **kwargs):
        """
        Insert a record into the database table.
        Handles `null`, `blank`, `default` parameters and checks for unique constraints.
        """
        if not kwargs:
            raise ValueError("No valid fields to insert.")

        missing_fields = []  # List to track missing required fields

        try:
            # Step 1: Get model fields
            model_fields = {
                name: field for name, field in cls.__dict__.items() if isinstance(field, Field)
            }

            # Step 2: Remove auto-generated 'id' field if present in kwargs
            if "id" in kwargs:
                kwargs.pop("id")  # Remove id from kwargs, as it is auto-generated by the database

            # Step 3: Validate and prepare data
            for name, field in model_fields.items():
                # Skip validation for primary key fields
                if getattr(field, "primary_key", True) and getattr(field, "autoincrement", True):
                    continue

                if name not in kwargs:  # Field not provided by the user
                    if getattr(field, "default", None) is not None:  # Use default if explicitly set
                        kwargs[name] = field.default
                    elif field.null:  # Allow NULL if 'null=True'
                        kwargs[name] = None
                    elif field.blank:  # Allow empty string if 'blank=True'
                        kwargs[name] = ""
                    else:
                        # Track missing required fields
                        missing_fields.append(name)

            if missing_fields:
                # Raise error if any required field is missing
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Step 4: Validate field types
            cls.validate_fields(kwargs)

            # Step 5: Build SQL query
            columns = ", ".join(kwargs.keys())
            placeholders = ", ".join(["?"] * len(kwargs))
            values = tuple(kwargs.values())
            sql = f"INSERT INTO {cls.table_name or cls.__name__.lower()} ({columns}) VALUES ({placeholders})"

            # Step 6: Execute SQL query
            affected_rows = cls._execute_sql(sql, values)
            if affected_rows == 0:
                if verbose:
                    print("No rows were inserted into the database.")
                return
            if verbose:
                print(f"Record inserted into table '{cls.table_name or cls.__name__.lower()}': {kwargs}")

        except ValueError as ve:
            print(f"Validation error: {ve}")
            raise  # Ensure ValueError is re-raised
        except TypeError as te:
            print(f"Type error: {te}")
            raise
        except sqlite3.Error as e:
            print(f"Database error while inserting record: {e}")

        except sqlite3.IntegrityError as e:
            raise ValueError(f"Integrity error: {e}") from e

        except Exception as e:
            print(f"Unexpected error in insert method: {e}")
            raise

    @classmethod
    def bulk_insert(cls, records):
        """
        Insert multiple records into the database table in a single query.
        :param records: A list of dictionaries where each dictionary represents a record to insert.
        :raises ValueError: If records are empty or validation fails.
        """
        if not records:
            raise ValueError("The records list cannot be empty for bulk insert.")

        try:
            # Step 1: Get model fields
            model_fields = {
                name: field for name, field in cls.__dict__.items() if isinstance(field, Field)
            }

            # Step 2: Preprocess field requirements
            all_columns = list(model_fields.keys())
            if 'id' in all_columns:  # Skip auto-generated 'id' field
                all_columns.remove('id')

            required_fields = {
                name for name, field in model_fields.items()
                if not field.null and getattr(field, "default", None) is None and name != "id"
            }
            default_values = {
                name: field.default for name, field in model_fields.items() if
                getattr(field, "default", None) is not None
            }

            # Step 3: Prepare columns and values
            placeholders = ", ".join(["?"] * len(all_columns))  # e.g., "?, ?, ?"
            columns = ", ".join(all_columns)  # e.g., "name, age, email"

            values_to_insert = []
            for record in records:
                row_values = {}
                for column in all_columns:
                    value = record.get(column, None)

                    # Use default value if not provided
                    if value is None:
                        if column in default_values:
                            value = default_values[column]
                        elif column in required_fields:
                            raise ValueError(f"Field '{column}' is required and must be provided.")

                    row_values[column] = value

                # Step 4: Validate the record
                cls.validate_fields(row_values)  # Use validate_fields method here

                # Append validated record as tuple
                values_to_insert.append(tuple(row_values[column] for column in all_columns))

            # Step 5: Build and execute the bulk insert SQL query
            sql = f"INSERT INTO {cls.table_name or cls.__name__.lower()} ({columns}) VALUES ({placeholders})"

            # Execute the query for all records at once
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.executemany(sql, values_to_insert)  # Use executemany for bulk insert
            conn.commit()
            conn.close()

            print(f"{len(records)} records inserted into table '{cls.table_name or cls.__name__.lower()}'.")
        except sqlite3.Error as e:
            print(f"Database error while performing bulk insert: {e}")
            raise
        except ValueError as ve:
            print(f"Validation error during bulk insert: {ve}")
            raise
        except TypeError as te:
            print(f"Type error during bulk insert: {te}")
            raise
        except Exception as e:
            print(f"Unexpected error in bulk_insert method: {e}")
            raise

    @classmethod
    def all(cls):
        """
        Retrieve all records from the table and return them as a QuerySet.
        """
        try:
            sql = f"SELECT * FROM {cls.table_name}"
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.close()

            # Retrieve field names dynamically from the model
            field_names = [name for name, field in cls.__dict__.items() if isinstance(field, Field)]

            objects = []
            for row in rows:
                # Map field names to row values dynamically
                obj_data = {field_names[i]: row[i] for i in range(len(field_names))}
                obj = cls(**obj_data)  # Create model instance using dynamic field mapping
                objects.append(obj)

            return QuerySet(cls, objects)

        except sqlite3.Error as e:
            print(f"Database error while retrieving records: {e}")
        except Exception as e:
            print(f"Unexpected error in all method: {e}")
            return QuerySet(cls, [])

    @classmethod
    def update(cls, filters, **updates):
        """
        Update records in the table that match the given filters.
        :param filters: A dictionary of conditions for filtering rows (e.g., {"age": 30}).
        :param updates: A dictionary of column names and their new values.
        """
        if not updates:
            raise ValueError("You must provide at least one column to update.")

        if not filters or not isinstance(filters, dict) or len(filters) == 0:
            raise ValueError("You must provide at least one condition in filters.")

        try:
            # Validate field types before proceeding
            cls.validate_fields(updates)

            # Prepare the SET clause for the SQL query
            set_clause = ", ".join([f"{column} = ?" for column in updates.keys()])
            values = list(updates.values())  # Values for the SET clause

            # Prepare the WHERE clause
            conditions = [f"{column} = ?" for column in filters.keys()]
            where_clause = f" WHERE {' AND '.join(conditions)}"
            values.extend(filters.values())  # Adding filter conditions to the values

            # Build the SQL query
            sql = f"UPDATE {cls.table_name or cls.__name__.lower()} SET {set_clause}{where_clause}"

            # Execute the SQL and get the number of affected rows
            affected_rows = cls._execute_sql(sql, values)

            # Check if any records were affected
            if affected_rows == 0:
                print(f"No records found matching filters: {filters}")
                return 0  # Return 0 if no records were updated
            else:
                print(f"Updated {affected_rows} records in table '{cls.table_name}' with filters: {filters}")
                return affected_rows

        except sqlite3.Error as e:
            print(f"Database error while updating records in table '{cls.table_name or cls.__name__.lower()}': {e}")
            return 0  # Return 0 for database error
        except ValueError as ve:
            print(f"Validation error: {ve}")
            raise
        except TypeError as te:
            print(f"Type error: {te}")
            raise
        except Exception as e:
            print(f"Unexpected error in update method: {e}")
            raise

    @classmethod
    def delete(cls, **filters):
        """
        Delete records from the database table based on filters.
        :param filters: A dictionary of conditions for filtering rows to delete.
        """
        if not filters:
            raise ValueError("Delete operation requires at least one condition (filter).")

        try:
            where_conditions = [f"{key} = ?" for key in filters.keys()]
            where_clause = f" WHERE {' AND '.join(where_conditions)}"
            values = list(filters.values())

            sql = f"DELETE FROM {cls.table_name or cls.__name__.lower()}{where_clause}"
            # Execute the SQL and get the number of affected rows

            affected_rows = cls._execute_sql(sql, values)

            # Check if any records were affected
            if affected_rows == 0:
                print(f"No records found matching filters: {filters}")
                return 0
            else:
                print(f"Deleted {affected_rows} records from table '{cls.table_name}' with filters: {filters}")
                return affected_rows

        except sqlite3.Error as e:
            print(f"Error deleting records from table '{cls.table_name or cls.__name__.lower()}': {e}")
            return 0
        except Exception as e:
            print(f"Unexpected error in delete method: {e}")
            return 0

    @classmethod
    def filter(cls, **filters):
        """
        Retrieve filtered records from the database table.
        :param filters: A dictionary of conditions for filtering rows.
        """
        if not filters:
            raise ValueError("Filter operation requires at least one condition (filter).")

        # Validate fields
        model_fields = {name for name, field in cls.__dict__.items() if isinstance(field, Field)}
        for field in filters.keys():
            if field not in model_fields:
                raise ValueError(f"Field '{field}' does not exist in the model.")

        try:
            where_clause = ""
            values = []
            if filters:
                where_conditions = [f"{key} = ?" for key in filters.keys()]
                where_clause = f" WHERE {' AND '.join(where_conditions)}"
                values = list(filters.values())  # Add values from filters

            sql = f"SELECT * FROM {cls.table_name or cls.__name__.lower()}{where_clause}"
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute(sql, values)  # Execute SQL with the values
            rows = cursor.fetchall()  # Get all rows
            conn.close()

            # Dynamically map rows to field names
            field_names = [name for name, field in cls.__dict__.items() if isinstance(field, Field)]
            objects = [cls(**dict(zip(field_names, row))) for row in rows]

            return QuerySet(cls, objects)

        except sqlite3.Error as e:
            print(f"Error filtering records in table '{cls.table_name or cls.__name__.lower()}': {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in filter method: {e}")
            return QuerySet(cls, [])

    @classmethod
    def add_field(cls, name, field):
        """
        Add a new column to the database table.
        """

        table_name = cls.table_name or cls.__name__.lower()

        # Step 1: Check if the table has records
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        record_count = cursor.fetchone()[0]

        # Step 2: If the table has records, ensure `null=True` and `blank=True`
        raised = False
        if record_count > 0:
            if not field.null:
                raised = True
                # raise ValueError(
                #                  f"Cannot add field '{name}' to table '{table_name}' with existing records "
                #                  f"unless `null=True`"
                #              )

        conn.close()

        try:
            sql = f"ALTER TABLE {table_name} ADD COLUMN {name} {field.db_type}"
            cls._execute_sql(sql)
            print(f"Field '{name}' added to table '{table_name}'.")
        except sqlite3.Error as e:
            print(f"Error adding field '{name}' to table '{table_name}': {e}")
        except Exception as e:
            print(f"Unexpected error in add_field method: {e}")
        finally:
            if raised:
                raise ValueError(
                    f"Cannot add field '{name}' to table '{table_name}' with existing records "
                    f"unless `null=True`"
                )
        # if raised:
        #     return False
        # else:
        #     return True

    @classmethod
    def get_existing_columns(cls):
        """
        Retrieve the list of existing columns in the table.
        """
        table_name = cls.table_name or cls.__name__.lower()

        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Use PRAGMA to get table column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = {row[1] for row in cursor.fetchall()}  # row[1] contains column name

            conn.close()
            return columns

        except sqlite3.Error as e:
            print(f"Database error while fetching columns for table '{table_name}': {e}")
            return set()
        except Exception as e:
            print(f"Unexpected error in get_existing_columns method: {e}")
            return set()

    @classmethod
    def sync_fields(cls):
        """
        Synchronize the model fields with the database table structure,
        adding new columns if needed and handling errors during the process.
        """
        table_name = cls.table_name or cls.__name__.lower()
        msg = ""
        raised = False

        try:
            # Get existing columns using the helper method
            existing_columns = cls.get_existing_columns()

            # Fetch model-defined fields
            model_fields = {
                name: field for name, field in cls.__dict__.items() if isinstance(field, Field)
            }

            # Identify new fields to be added
            new_fields = {
                name: field for name, field in model_fields.items() if name not in existing_columns
            }

            # Add new fields
            if new_fields:
                for name, field in new_fields.items():
                    try:
                        # if cls.add_field(name, field):
                        #     print(f"Column '{name}' added to table '{table_name}'.")
                        # else:
                        #     raised = True
                        cls.add_field(name, field)
                        print(f"Column '{name}' added to table '{table_name}'.")
                    except Exception as e:
                        print(f"Error adding column '{name}' to table '{table_name}': {e}")

            else:
                msg += f"No updates needed for table '{table_name}'."

        except sqlite3.Error as e:
            print(f"Database error while synchronizing fields for table '{table_name}': {e}")
        except Exception as e:
            print(f"Unexpected error during synchronization: {e}")
        finally:
            # if raised:
            #     raise ValueError

            if msg != "":
                return False, msg
            else:
                return True, True

    @classmethod
    def remove_missing_columns(cls):
        """
        Remove columns from the database table that are no longer defined in the model.
        """
        conn = None
        msg = ""
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            table_name = cls.table_name or cls.__name__.lower()

            # Fetch existing columns
            try:
                cursor.execute(f"PRAGMA table_info({table_name})")
                existing_columns = {row[1] for row in cursor.fetchall()}
            except sqlite3.Error as e:
                print(f"Error fetching columns from table '{table_name}': {e}")
                return  # Exit the method early if this step fails

            # Fetch model-defined columns
            model_fields = {
                name: field for name, field in cls.__dict__.items() if isinstance(field, Field)
            }

            # Identify columns to drop
            columns_to_drop = existing_columns - model_fields.keys()

            if columns_to_drop:
                msg += f"Removing columns from table '{table_name}': {', '.join(columns_to_drop)}"
                # Remaining columns
                remaining_columns = existing_columns - columns_to_drop

                # Fetch column definitions from the model
                remaining_definitions = [
                    f"{name} {model_fields[name].db_type}" for name in remaining_columns
                ]
                remaining_columns_sql = ", ".join(remaining_definitions)

                # Temporary table name
                temp_table = f"{table_name}_temp"

                # Create a temporary table
                try:
                    cursor.execute(f"CREATE TABLE {temp_table} ({remaining_columns_sql})")
                except sqlite3.Error as e:
                    print(f"Error creating temporary table '{temp_table}': {e}")
                    return  # Exit the method early if this step fails

                # Copy data to the temporary table
                columns_to_copy = ", ".join(remaining_columns)
                try:
                    cursor.execute(
                        f"INSERT INTO {temp_table} ({columns_to_copy}) SELECT {columns_to_copy} FROM {table_name}")
                except sqlite3.Error as e:
                    print(f"Error copying data to temporary table '{temp_table}': {e}")
                    return  # Exit the method early if this step fails

                # Drop the old table
                try:
                    cursor.execute(f"DROP TABLE {table_name}")
                except sqlite3.Error as e:
                    print(f"Error dropping table '{table_name}': {e}")
                    return  # Exit the method early if this step fails

                # Rename the temporary table to the original table name
                try:
                    cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
                except sqlite3.Error as e:
                    print(f"Error renaming table '{temp_table}' to '{table_name}': {e}")
                    return  # Exit the method early if this step fails

            conn.commit()

        except sqlite3.Error as e:
            print(f"Database error while removing columns: {e}")
        except Exception as e:
            print(f"Unexpected error in remove_missing_columns method: {e}")
        finally:
            if conn:
                conn.close()
            if msg != "":
                # result = [True, msg]
                return True, msg
            else:
                return False, False
