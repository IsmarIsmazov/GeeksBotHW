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
        self.connection.execute(sql_queries.CREATE_USER_FORM_TABLE_QUERY)
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

    def sql_select_user_by_id(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {'id': row[0]}
        return self.cursor.execute(sql_queries.SELECT_USER_BY_TELEGRAM_ID_QUERY, (telegram_id,)).fetchall()

    def sql_insert_user_form(self, telegram_id, username, groop, idea, proglem):
        self.cursor.execute(sql_queries.INSERT_USER_FORM_QUERY, (
            None, telegram_id, username, groop, idea, proglem
        ))
        self.connection.commit()

    def get_survey_by_id(self, survey_id):
        self.cursor.execute(sql_queries.QUERY_ID_USER_FORM, (survey_id,))
        return self.cursor.fetchone()

    def sql_select_all_user_forms(self):
        self.cursor.row_factory = lambda cursor, row: {
            'id': row[0],
            'telegram_id': row[1],
            'username': row[2],
            'groop': row[3],
            'idea': row[4],
            'proglem': row[5]
        }
        return self.cursor.execute(sql_queries.SELECT_USERS_FORM_QUERY).fetchall()
