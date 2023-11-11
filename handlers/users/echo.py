from aiogram import types

from loader import dp


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)

# import sqlite3
#
# conn = sqlite3.connect("users.db")
# cursor = conn.cursor()
#
# cursor.execute("DROP TABLE users")
#
# conn.commit()
