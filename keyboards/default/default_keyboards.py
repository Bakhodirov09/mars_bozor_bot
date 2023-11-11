from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tel_nomer = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Telefon Raqamni Jonatish", request_contact=True)
        ]
    ], resize_keyboard=True
)

register = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🪪 Ro'yxatdan O'tish")
        ]
    ], resize_keyboard=True
)

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⌨️ Mening Mahsulotlarim"),
            KeyboardButton(text="🚀 Mars Bozor")
        ],
        [
            KeyboardButton(text="🛒 Bozor Tarixi"),
            KeyboardButton(text="📞 Aloqa")
        ]
    ], resize_keyboard=True
)

mars_bozor = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛒 Mahsulot Sotib Olish"),
            KeyboardButton(text="🛍 Mahsulot Sotish")
        ],
        [
            KeyboardButton(text="🏘 Asosiy Menyu")
        ]
    ], resize_keyboard=True
)

my_products = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Mahsulot Qoshish"),
            KeyboardButton(text="🛍 Mening Mahsulotlarim")
        ],
        [
            KeyboardButton(text="🏘 Asosiy Menyuga Qaytish")
        ]
    ], resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏘 Asosiy Menyuga Qaytish")
        ]
    ], resize_keyboard=True
)