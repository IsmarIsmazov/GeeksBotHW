import sqlite3

from aiogram import types, Dispatcher
from config import bot
from const import START_TEXT
from database.sql_commands import Database
from keyboards.inline_buttons import start_keyboard


async def start_button(message: types.Message):
    # try:
    db = Database()
    db.sql_insert_user_command(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    # except sqlite3.IntegrityError:
    #     pass

    await bot.send_message(
        chat_id=message.chat.id,
        text=START_TEXT.format(
            username=message.from_user.username
        ),
        parse_mode=types.ParseMode.MARKDOWN_V2,
        reply_markup=await start_keyboard()
    )

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
