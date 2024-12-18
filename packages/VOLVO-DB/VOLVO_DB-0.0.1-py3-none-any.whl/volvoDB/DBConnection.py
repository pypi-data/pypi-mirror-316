import sqlite3

class DBConnection:
    _db_instance = None

    def __init__(self):
        self.connection = None

    @staticmethod
    def get_instance(db_path):
        if DBConnection._db_instance is None:
            DBConnection._db_instance = DBConnection()
            DBConnection._db_instance.connection = sqlite3.connect(db_path, check_same_thread=False)
            DBConnection._db_instance.connection.row_factory = sqlite3.Row
        return DBConnection._db_instance.connection

    @staticmethod
    def pdo_instance(db_path):
        try:
            connection = sqlite3.connect(db_path, check_same_thread=False)
            connection.row_factory = sqlite3.Row
            return connection
        except sqlite3.Error as e:
            DBConnection.log_error('DATABASE', str(e))
            return None

    @staticmethod
    def log_error(context, message):
        print(f"[{context}] Error: {message}")