from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.database import DatabaseManager

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, proxy="http://proxy.server:3128")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_manager = DatabaseManager("users.db")
from handlers import *
