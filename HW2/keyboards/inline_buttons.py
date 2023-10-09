from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_keyboard():
    markup = InlineKeyboardMarkup()
    questionnaire_button = InlineKeyboardButton(
        "Узнать",
        callback_data="start Questionnaire"
    )
    markup.add(
        questionnaire_button
    )
    return markup


async def question_first_keyboard():
    markup = InlineKeyboardMarkup()
    male_button = InlineKeyboardButton(
        "Кошки",
        callback_data="cats_answer"
    )
    female_button = InlineKeyboardButton(
        "Собаки",
        callback_data="dogs_answer"
    )
    markup.add(
        male_button
    ).add(female_button)
    return markup
