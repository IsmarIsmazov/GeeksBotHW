import sqlite3
from database import sql_queries


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")
        self.cursor = self.connection.cursor()

    def sql_create(self):
        if self.connection:
            print('Database connected')
        self.connection.execute(sql_queries.CREATE_USER_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_RESPONSES_TABLE_QUERY)

    def sql_insert_user_command(self, telegram_id, username, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, username, first_name, last_name,)
        )
        self.connection.commit()

    def sql_insert_user_response(self, telegram_id, response_text):
        self.cursor.execute(
            sql_queries.INSERT_RESPONSE_QUERY,
            (telegram_id, response_text,)
        )
        self.connection.commit()