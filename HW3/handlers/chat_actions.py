import datetime
from config import bot, GROUP_ID, ADMIN_ID
from aiogram import types, Dispatcher
from database.sql_commands import Database


async def echo_ban(message: types.Message):
    ban_words = ['fuck', 'bitch', 'damn']
    if message.chat.id in GROUP_ID:
        for word in ban_words:
            if word in message.text.lower():
                user_id = message.from_user.id

                if user_id in ADMIN_ID:
                    return

                ban_user = Database().sql_select_ban_user_command(telegram_id=user_id)

                if ban_user:
                    Database().sql_update_ban_user_count_command(telegram_id=user_id)
                    await bot.send_message(chat_id=user_id, text='Пожалуйста, не используйте ругательства.')
                else:
                    Database().sql_insert_ban_user_command(telegram_id=user_id)
                    await bot.send_message(chat_id=user_id, text='Пожалуйста, не используйте ругательства.')

                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

                if message.text == '/list_ban_users' and user_id in ADMIN_ID:
                    ban_users = Database().sql_select_all_ban_users()
                    if ban_users:
                        response_text = "Пользователи в списке потенциальных банов:\n"
                        for user in ban_users:
                            response_text += f"User ID: {user['telegram_id']}, Count: {user['count']}\n"
                        await bot.send_message(chat_id=user_id, text=response_text)


def register_chat_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_ban)
