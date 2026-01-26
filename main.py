from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from dialogs.main_dialog import main_menu_dialog
from dialogs.keyway_first_lesson_dialog import keyway_first_lesson_dialog
from handlers.start_handler import main_menu_router
from config.config import load_config


config = load_config()
storage = MemoryStorage()

api = TelegramAPIServer.from_base(
        "http://127.0.0.1:8081",
        is_local=True,  # поставьте True, если ваш telegram-bot-api запущен с --local
    )
session = AiohttpSession(api=api)

bot = Bot(token=config.tg_bot.token, session=session)

# bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(storage=storage)

dp.include_router(main_menu_router)
dp.include_routers(main_menu_dialog, keyway_first_lesson_dialog)

setup_dialogs(dp)







if __name__ == '__main__':
    dp.run_polling(bot)