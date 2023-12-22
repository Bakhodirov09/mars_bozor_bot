from aiogram import executor, types

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import *
db_manager = DatabaseManager("users.db")
async def on_startup(dispatcher, message: types.Message):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)
    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    db_manager.create_table(chat_id=message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
