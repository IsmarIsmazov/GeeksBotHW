from decouple import config as env
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage =MemoryStorage()
TOKEN = env("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
ADMIN_ID = [1539786534, ]
BOT_PIC = "/Users/ismarhahazov/GeeksBot/lesson2/media/bot_pic.jpeg"
ANIMATION_PIC = "/Users/ismarhahazov/GeeksBot/lesson2/media/animation_pic.gif"
GROUP_ID = [-4056197755, ]