import sqlite3
from .abstract import DataBaseBackend
from dbeasyorm.fields import BaseField, ForeignKey


class SQLiteBackend(DataBaseBackend):
    def __init__(self, database_path: str, *args, **kwargs):
        self.database_path = database_path
        self.cursor = None
        self.connection = None
        self.type_map = self.get_sql_types_map()

    def get_placeholder(self) -> str:
        return "?"

    def get_sql_type(self, type) -> str:
        return self.type_map.get(type)

    def get_sql_types_map(self) -> dict:
        return {
            int: "INTEGER",
            float: "REAL",
            bytes: "BLOB",
            bool: "INTEGER",
            str: "TEXT"
        }

    def get_foreign_key_constraint(self, field_name: str, related_table: str, on_delete: str) -> str:
        return (
            f"{field_name} INTEGER ",
            f"FOREIGN KEY ({field_name}) REFERENCES {related_table} (_id) "
            f"ON DELETE {on_delete}"
        )

    def connect(self, **kwargs) -> DataBaseBackend:
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        return self

    def execute(self, query: str, params=None) -> sqlite3.Cursor:
        # Split the query into individual statements and execute them
        statements = query.strip().split(";")
        for statement in statements:
            if statement.strip():
                self.cursor.execute(statement.strip(), params or ())
        self.connection.commit()
        return self.cursor

    def generate_insert_sql(self, table_name: str, columns: tuple) -> str:
        columns_str = ', '.join(columns)
        placeholders = ', '.join([self.get_placeholder() for _ in columns])
        return f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    def generate_select_sql(self, table_name: str, columns: tuple, where_clause: dict = None, limit: int = None, offset: int = None) -> str:
        where_sql = ""
        if where_clause:
            where_sql = " WHERE " + " AND ".join([f"{col} = " + self.get_sql_val_repr(val) for col, val in where_clause.items()])

        limit_offset_sql = ""
        if limit is not None:
            limit_offset_sql = f" LIMIT {limit}"
        if offset is not None:
            limit_offset_sql += f" OFFSET {offset}"

        return f"SELECT {', '.join(columns) if columns else f'{table_name}.*'} FROM {table_name}{where_sql}{limit_offset_sql}"

    def generate_join_sql(self, table_name: str, on: str, join_type: str) -> str:
        return f" {join_type} JOIN {table_name} ON {on}"

    def generate_update_sql(self, table_name: str, set_clause: tuple, where_clause: tuple):
        set_sql = ', '.join([f"{col}={self.get_placeholder()}" for col in set_clause])
        where_sql = " AND ".join([f"{col}={self.get_placeholder()}" for col in where_clause]) if where_clause else ""
        return f"UPDATE {table_name} SET {set_sql} WHERE {where_sql}"

    def generate_delete_sql(self, table_name: str, where_clause: tuple):
        where_sql = " AND ".join([f"{col}={self.get_placeholder()}" for col in where_clause]) if where_clause else ""
        return f"DELETE FROM {table_name} WHERE {where_sql}"

    def generate_create_table_sql(self, table_name: str, fields: BaseField):
        columns = []
        foreign_keys = []

        for field in fields:
            if isinstance(field, ForeignKey):
                column, foreign_key = field.get_sql_line(self.get_foreign_key_constraint)
                columns.append(column)
                foreign_keys.append(foreign_key)
            else:
                columns.append(
                    field.get_sql_line(sql_type=self.get_sql_type(field.python_type))
                )
        table_body = ", \n".join(columns + foreign_keys)
        return f"""CREATE TABLE IF NOT EXISTS {table_name} ({table_body});"""

    def generate_alter_field_sql(self, model: BaseField, db_columns: dict, *args, **kwargs) -> str:
        table_name = model.query_creator.get_table_name()
        sql_result = ''
        db_columns = ", ".join(db_columns.keys())

        # sql_create_new_table_query
        sql_result += self.generate_create_table_sql(f"{table_name}_NEW", list(model._fields.values()))
        sql_result += f"""INSERT INTO {table_name}_NEW ({db_columns}) SELECT {db_columns} FROM {table_name};"""
        sql_result += self.generate_drop_table_sql(table_name=table_name)
        sql_result += f"ALTER TABLE {table_name}_NEW RENAME TO {table_name};"
        return sql_result

    def generate_drop_field_sql(self, model: BaseField, *args, **kwargs) -> str:
        table_name = model.query_creator.get_table_name()
        sql_result = ''
        columns = ", ".join(model._fields.keys())

        # sql_create_new_table_query
        sql_result += self.generate_create_table_sql(f"{table_name}_NEW", list(model._fields.values()))
        sql_result += f"""INSERT INTO {table_name}_NEW ({columns}) SELECT {columns} FROM {table_name};"""
        sql_result += self.generate_drop_table_sql(table_name=table_name)
        sql_result += f"ALTER TABLE {table_name}_NEW RENAME TO {table_name};"
        return sql_result

    def generate_drop_table_sql(self, table_name: str) -> str:
        return f"DROP TABLE {table_name};"

    def get_database_schemas(self) -> dict:
        schema = {}

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        for table in tables:
            table_name = table[0]
            if table_name == 'sqlite_sequence':
                continue

            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns = self.cursor.fetchall()
            schema[table_name] = {col[1]: col[2] for col in columns}

        return schema
