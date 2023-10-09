from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import Database
from keyboards.inline_buttons import question_first_keyboard


async def start_questionnarie_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Кошки или Собаки?",
        reply_markup=await question_first_keyboard()
    )


async def male_questionnarie_call(call: types.CallbackQuery):
    user_id = call.from_user.id
    response = "Кошки"
    db = Database()
    db.sql_insert_user_response(user_id, response)

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Кошки и вправду милые",
    )


async def female_questionnarie_call(call: types.CallbackQuery):
    user_id = call.from_user.id
    response = "собаки"
    db = Database()
    db.sql_insert_user_response(user_id, response)

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Собауи! круто!",
    )


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnarie_call, lambda call: call.data == "start Questionnaire")
    dp.register_callback_query_handler(male_questionnarie_call, lambda call: call.data == "cats_answer")
    dp.register_callback_query_handler(female_questionnarie_call, lambda call: call.data == "dogs_answer")
