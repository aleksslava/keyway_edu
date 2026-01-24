from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from dialogs.main_dialog import main_menu_dialog
from dialogs.keyway_first_lesson_dialog import keyway_first_lesson_dialog
from handlers.start_handler import main_menu_router
from config.config import load_config


config = load_config()
storage = MemoryStorage()
bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(storage=storage)

dp.include_router(main_menu_router)
dp.include_routers(main_menu_dialog, keyway_first_lesson_dialog)

setup_dialogs(dp)







if __name__ == '__main__':
    dp.run_polling(bot)