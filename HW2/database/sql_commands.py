import sqlite3
from database import sql_queries


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")
        self.cursor = self.connection.cursor()

    # Комманда создание таблиц в БД
    def sql_create(self):
        if self.connection:
            print('Database connected')
        self.connection.execute(sql_queries.CREATE_USER_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_RESPONSES_TABLE_QUERY)

    # Комманда для сохранение в бд
    def sql_insert_user_command(self, telegram_id, username, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, username, first_name, last_name,)
        )
        self.connection.commit()

    # Комманда для сохранение в бд
    def sql_insert_user_response(self, telegram_id, response_text):
        self.cursor.execute(
            sql_queries.INSERT_RESPONSE_QUERY,
            (telegram_id, response_text,)
        )
        self.connection.commit()

    # SQL комманды для таблицы бан
    def sql_insert_ban_user_command(self, telegram_id):
        self.cursor.execute(
            sql_queries.INSERT_BAN_USER_QUERY,
            (None, telegram_id, 1,)
        )
        self.connection.commit()

    def sql_select_ban_user_command(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            'id': row[0],
            'telegram_id': row[1],
            'count': row[2]
        }
        return self.cursor.execute(
            sql_queries.SELECT_BAN_USER_QUERY,
            (None, telegram_id)
        ).fetchall()

    def sql_update_ban_user_count_command(self, telegram_id):
        self.cursor.execute(
            sql_queries.INSERT_BAN_USER_QUERY,
            (telegram_id)
        )
        self.connection.commit()

    def sql_select_all_ban_users(self):
        self.cursor.row_factory = lambda cursor, row: {
            'telegram_id': row[1],
            'count': row[2]
        }
        return self.cursor.execute("SELECT * FROM ban_users").fetchall()
