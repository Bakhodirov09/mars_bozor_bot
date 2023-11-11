from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.default_keyboards import *
from loader import dp


@dp.message_handler(text="❌ Bekor Qilish", state="*")
async def cancelling(message: types.Message, state: FSMContext):
    text = "❌ Bekor Qilindi"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()