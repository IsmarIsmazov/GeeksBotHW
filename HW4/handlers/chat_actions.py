import datetime

from config import bot, GROUP_ID
from aiogram import types, Dispatcher

from database.sql_commands import Database


async def complain_user(message: types.Message):
    # Получите username цели жалобы и причину
    args = message.get_args().split()
    if len(args) < 2:
        await message.reply("Использование: /complaint <username> <причина>")
        return

    target_username = args[0]
    reason = " ".join(args[1:])

    # Найдите пользователя с таким username в базе данных
    user = Database().sql_select_user_by_username(target_username)

    if user:
        user_id = message.from_user.id
        target_telegram_id = user[1]

        existing_complaint = Database().sql_select_complaint(user_id, target_telegram_id)
        if existing_complaint:
            Database().sql_update_complaint_count(
                targe_telegram_id=message.from_user.id,
            )
        else:
            Database().sql_insert_complaint(user_id, target_telegram_id, reason)

        if existing_complaint and existing_complaint[4] >= 3:
            await bot.kick_chat_member(chat_id=message.chat.id, user_id=target_telegram_id)
            await message.reply(f"Пользователь с username {target_username} забанен за множественные жалобы.")
        else:
            await message.reply("Жалоба отправлена.")
    else:
        await message.reply("Пользователь с таким username не найден.")


async def echo_ban(message: types.Message):
    ban_words = ['fuck', 'bitch', 'damn']
    if message.chat.type == types.ChatType.GROUP or message.chat.type == types.ChatType.SUPERGROUP:
        for word in ban_words:
            if word in message.text.lower().replace(" ", ' '):
                ban_user = Database().sql_select_ban_user_command(
                    telegram_id=message.from_user.id,
                )
                if ban_user and ban_user[0]['count'] >= 3:
                    user_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
                    await bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
                elif ban_user:
                    Database().sql_update_ban_user_count_command(
                        telegram_id=message.from_user.id,
                    )
                else:
                    Database().sql_insert_ban_user_command(
                        telegram_id=message.from_user.id
                    )
                await  bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                )
                await bot.send_message(
                    chat_id=message.chat.id,
                    text='hey dont use bad words',
                )
                # await bot.ban_chat_memder(
                #     chat_id=message.chat.id,
                #     user_id=message.from_user.id,
                #     until_date=datetime.datetime.now() + datetime.timedelta(minutes=1)
                # )


def register_chat_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(complain_user, commands=['complaint'])
    dp.register_message_handler(echo_ban)
