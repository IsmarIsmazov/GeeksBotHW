# Таблица для сохранение пользователей
CREATE_USER_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS telegram_users
        (ID INTEGER PRIMARY KEY,
         TELEGRAM_ID INTEGER,
         USERNAME CHAR(50),
         FIRST_NAME CHAR(50),
         LAST_NAME CHAR(50),
         UNIQUE(TELEGRAM_ID)
         )
"""

INSERT_USER_QUERY = """INSERT OR IGNORE INTO telegram_users VALUES (?,?,?,?,?)"""


# Таблица для сохранение ответов
CREATE_RESPONSES_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS user_responses
        (ID INTEGER PRIMARY KEY,
         TELEGRAM_ID INTEGER,
         RESPONSE_TEXT TEXT,
         FOREIGN KEY (TELEGRAM_ID) REFERENCES telegram_users(TELEGRAM_ID)
         )
"""
INSERT_RESPONSE_QUERY = """INSERT INTO user_responses (TELEGRAM_ID, RESPONSE_TEXT) VALUES (?, ?)"""


# Таблица для банов
CREATE_BAN_USER_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS ban_users
        (ID INTEGER PRIMARY KEY,
         TELEGRAM_ID INTEGER,
         COUNT INTEGER,
         UNIQUE(TELEGRAM_ID)
         )
"""

INSERT_BAN_USER_QUERY = """INSERT OR IGNORE INTO ban_users VALUES (?,?,?)"""

SELECT_BAN_USER_QUERY = """SELECT * FROM ban_users WHERE TELEGRAM_ID = ?"""

UPDATE_BAN_USER_COUNT_QUERY = """UPDATE ban_users SET COUNT = COUNT + 1 WHERE TELEGRAM_ID = ?"""
