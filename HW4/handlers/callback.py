from aiogram import types, Dispatcher
from config import bot
from const import START_TEXT
from database.sql_commands import Database
from keyboards.inline_buttons import question_first_keyboard


async def start_questionnarie_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Male or Female",
        reply_markup=await question_first_keyboard()
    )


async def male_questionnarie_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="yes you are male",
    )


async def female_questionnarie_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="yes you area female",
    )


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnarie_call, lambda call: call.data == "start Questionnaire")
    dp.register_callback_query_handler(male_questionnarie_call, lambda call: call.data == "male_answer")
    dp.register_callback_query_handler(female_questionnarie_call, lambda call: call.data == "female_answer")
