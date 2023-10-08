from decouple import config as env
from aiogram import Bot, Dispatcher

TOKEN = env("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
