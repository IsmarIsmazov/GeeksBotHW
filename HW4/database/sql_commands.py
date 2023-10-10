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
        self.connection.execute(sql_queries.CREATE_USER_FORM_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_TABLE_COMPLAINTS_QUERY)
        self.connection.execute(sql_queries.CREATE_BAN_USER_TABLE_QUERY)

    def sql_insert_user_command(self, telegram_id, username, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, username, first_name, last_name,)
        )
        self.connection.commit()

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
            (telegram_id,)
        ).fetchall()

    def sql_update_ban_user_count_command(self, telegram_id):
        self.cursor.execute(
            sql_queries.UPDATE_BAN_USER_COUNT_QUERY,
            (telegram_id,)
        )
        self.connection.commit()

    def sql_select_user_by_id(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {'id': row[0]}
        return self.cursor.execute(sql_queries.SELECT_USER_BY_ID_QUERY, (telegram_id,)).fetchall()

    def sql_insert_user_form(self, user_id, telegram_id, nickname, age, bio, gender, photo):
        self.cursor.execute(sql_queries.INSERT_USER_FORM_QUERY, (
            None, user_id, telegram_id, nickname, age, bio, gender, photo,
        ))
        self.connection.commit()

    # Запросы для таблизы жалобы
    def sql_select_complaint(self, user_id, target_telegram_id):
        self.cursor.execute(
            sql_queries.SELECT_COMPLAINT_QUERY,
            (user_id, target_telegram_id,)
        )
        return self.cursor.fetchone()

    def sql_insert_complaint(self, user_id, target_telegram_id, reason):
        self.cursor.execute(
            sql_queries.INSERT_COMPLAINT_QUERY,
            (None, user_id, target_telegram_id, reason, 1,)
        )
        self.connection.commit()

    def sql_select_user_by_username(self, username):
        self.cursor.execute(
            sql_queries.SELECT_USER_BY_USERNAME_QUERY,
            (username,)
        )
        return self.cursor.fetchone()

    def sql_update_complaint_count(self, targe_telegram_id):
        self.cursor.execute(
            sql_queries.UPDATE_COMPLAINT_USER_COUNT_QUERY,
            (targe_telegram_id, )
        )
        self.connection.commit()
