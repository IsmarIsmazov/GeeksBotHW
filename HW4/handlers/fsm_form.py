from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

from config import bot
from database.sql_commands import Database


class FormStates(StatesGroup):
    nickname = State()
    age = State()
    bio = State()
    gender = State()
    photo = State()


async def fsm_start(message: types.Message):
    await message.reply("send me your nickname")
    await FormStates.nickname.set()


async def load_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text
    await FormStates.next()
    await message.reply('send me your age, use oly numeric text')


async def load_age(message: types.Message, state: FSMContext):
    if type(int(message.text)) != int:
        await message.reply('please only numeric')
    else:
        async with state.proxy() as data:
            data['age'] = int(message.text)
        await FormStates.next()
        await message.reply('send me your bio')


async def load_bio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bio'] = message.text
    await FormStates.next()
    await message.reply("send me your gender")


async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await FormStates.next()
    await message.reply("send me your photo")


async def load_photo(message: types.Message, state: FSMContext):
    user_id = Database().sql_select_user_by_id(telegram_id=message.from_user.id)
    path = await message.photo[-1].download(destination_dir="/Users/ismarhahazov/GeeksBot/lesson3/media")
    async with state.proxy() as data:
        data['photo'] = path.name
    Database().sql_insert_user_form(
        user_id=user_id[0]['id'],
        telegram_id=message.from_user.id,
        nickname=data["nickname"],
        age=data["age"],
        bio=data["bio"],
        gender=data["gender"],
        photo=data["photo"],

    )
    await message.reply('you successful registration!')
    await state.finish()


def register_handler_fsm_form(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['signup'])
    dp.register_message_handler(load_nickname, state=FormStates.nickname, content_types=['text'])
    dp.register_message_handler(load_age, state=FormStates.age, content_types=['text'])
    dp.register_message_handler(load_bio, state=FormStates.bio, content_types=['text'])
    dp.register_message_handler(load_gender, state=FormStates.gender, content_types=['text'])
    dp.register_message_handler(load_photo, state=FormStates.photo, content_types=ContentType.PHOTO)
