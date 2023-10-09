import sqlite3

from aiogram import types, Dispatcher
from config import bot, BOT_PIC, ADMIN_ID
from const import START_TEXT
from database.sql_commands import Database
from keyboards.inline_buttons import start_keyboard


async def help_command(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Привет {message.from_user.first_name}!\n'
             f'Вот команды которые у нас есть: \n'
             f'/start - начать опрос о домашних животных\n'
             f'/photo - отправляет фотографию'
    )


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


async def show_surveys(message: types.Message):
    if message.chat.type == 'private' and message.from_user.id in ADMIN_ID:
        surveys = Database().sql_select_all_user_forms()

        for survey in surveys:
            await message.reply(
                f"Айди опроса: {survey['id']}\nГруппа: {survey['groop']}\nИдея: {survey['idea']}\nПроблема: {survey['proglem']}")

        await message.reply("Введите айди опроса, чтобы продолжить.")

    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text='Данная команда разрешена лишь для админов в личном чате')


async def process_survey_id(message: types.Message):
    survey_id = int(message.text)
    survey = Database().get_survey_by_id(survey_id)

    if survey:
        user_form_data = Database().get_survey_by_id(survey_id)

        if user_form_data:
            await message.reply(f"Данные из таблицы user_form для опроса с айди {survey_id}:\n{user_form_data}")
        else:
            await message.reply("В таблице user_form нет данных для этого опроса.")
    else:
        await message.reply(f"Опрос с айди {survey_id} не найден.")


async def send_photo(message: types.Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=BOT_PIC
    )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(send_photo, commands=['photo'])
    dp.register_message_handler(show_surveys, commands=['show_surveys'], state='*')
    dp.register_message_handler(process_survey_id, lambda message: message.text.isdigit(), state='*')
