class Field:
    def __init__(self, db_type, null=False, blank=False, unique=False, default=None):
        """
        :param db_type: Type of the field (e.g., "INTEGER", "VARCHAR(100)", etc.)
        :param null: Whether the field can store NULL in the database.
        :param blank: Whether the field can be left blank (for forms, etc.).
        """
        self.db_type = db_type
        self.null = null  # Whether the field can be NULL in the database
        self.blank = blank  # Whether the field can be left blank in forms
        self.unique = unique
        self.default = default
        self.expected_type = None  # To be defined in subclasses


class ForeignKey(Field):
    def __init__(self, related_model, on_delete="CASCADE"):

        self.related_model = related_model
        self.on_delete = on_delete
        super().__init__(db_type="INTEGER")
        self.expected_type = int


class IntegerField(Field):
    def __init__(self, primary_key=False, autoincrement=False, null=False, blank=False, unique=False, default=None):
        db_type = "INTEGER"
        if primary_key:
            db_type += " PRIMARY KEY"
        if autoincrement:
            db_type += " AUTOINCREMENT"
        super().__init__(db_type, null=null, blank=blank, unique=unique, default=default)
        self.expected_type = int


class CharField(Field):
    def __init__(self, max_length=255, default=None, null=False, blank=False, unique=False):
        super().__init__(f"VARCHAR({max_length})", null=null, blank=blank, default=default, unique=unique)
        self.expected_type = str


class BooleanField(Field):
    def __init__(self, default=False, null=False):
        super().__init__("BOOLEAN", default=default, null=null)
        self.expected_type = bool


class DateField(Field):
    def __init__(self, default=None, null=False, blank=False, unique=False):
        super().__init__("DATE", null=null, blank=blank, default=default, unique=unique)
        self.expected_type = str


class TextField(Field):
    def __init__(self, default=None, null=False, blank=False, unique=False):
        super().__init__("TEXT", default=default, null=False, blank=False, unique=unique)
        self.expected_type = str