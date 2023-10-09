from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

from config import bot
from database.sql_commands import Database


class FSMform(StatesGroup):
    username = State()
    groop = State()
    idea = State()
    problems = State()
    submit = State()


async def fsm_start(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Введите свое имя"
    )
    await FSMform.username.set()


async def load_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await FSMform.next()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Вы какой в группе?'
    )


async def load_groop(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['groop'] = message.text
    await FSMform.next()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Напишите идеи для бота, как можно его улучшить?'
    )


async def load_idea(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['idea'] = message.text
    await FSMform.next()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Напишите о проблемах бота, если они конечно есть'
    )


async def load_problem(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['problem'] = message.text
    await FSMform.next()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f'Имя: {data["username"]}\nГруппа: {data["groop"]}\n'
             f'Идея: {data["idea"]}\nПроблема: {data["problem"]}\n\n'
             f'Всё верно? \n'
    )


async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        user_id = Database().sql_select_user_by_id(telegram_id=message.from_user.id)
        async with state.proxy() as data:
            Database().sql_insert_user_form(
                telegram_id=user_id[0]['id'],
                username=data["username"],
                groop=data["groop"],
                idea=data["idea"],
                proglem=data["problem"],
            )
        await state.finish()
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Успешно сохранено в БД"
        )
    elif message.text.lower() == 'нет':
        await state.finish()
        await bot.send_message(
            chat_id=message.from_user.id,
            text="отменено"
        )
    else:
        await message.answer('Не пон')


async def cancel_help(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('отменено')


def register_fsm_form_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_help, state='*', commands=['cancel'])
    dp.register_message_handler(fsm_start, commands=['survey'])
    dp.register_message_handler(load_username, state=FSMform.username, content_types=['text'])
    dp.register_message_handler(load_groop, state=FSMform.groop, content_types=['text'])
    dp.register_message_handler(load_idea, state=FSMform.idea, content_types=['text'])
    dp.register_message_handler(load_problem, state=FSMform.problems, content_types=['text'])
    dp.register_message_handler(load_submit, state=FSMform.submit, content_types=['text'])
