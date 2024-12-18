from volvoDB.DBConnection import DBConnection
class DB:
    def __init__(self, connection):
        self.connection = connection
        self.table_name = None
        self.where_clause = ""
        self.where_values = []

    def table(self, table_name):
        self.table_name = table_name
        return self

    def get(self):
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {self.table_name} {self.where_clause}"
        cursor.execute(query, self.where_values)
        return cursor.fetchall()

    def insert(self, columns, values):
        cursor = self.connection.cursor()
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in values])
        sql = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        self.connection.commit()

    def where(self, column, value):
        self.where_clause = f"WHERE {column} = ?"
        self.where_values = [value]
        return self

    def first(self):
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {self.table_name} {self.where_clause}"
        cursor.execute(query, self.where_values)
        return cursor.fetchone()

    def update(self, columns, values):
        cursor = self.connection.cursor()
        updates = ', '.join([f"{col} = ?" for col in columns])
        sql = f"UPDATE {self.table_name} SET {updates} {self.where_clause}"
        cursor.execute(sql, values + self.where_values)
        self.connection.commit()