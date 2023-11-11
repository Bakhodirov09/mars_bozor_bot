from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_add = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Mahsulot Qoshishni Bekor Qilish!", callback_data="cancel")
        ]
    ]
)

write_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✍️ Adminga Botdan Yozish!", callback_data="admin_hand")
        ]
    ]
)

yes_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Xa Bozorga Qoyilsin", callback_data="yes")
        ],
        [
            InlineKeyboardButton(text="❌ Yoq Fikrimdan Qaytdim!", callback_data="no")
        ]
    ]
)

numbers = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="1"),
            InlineKeyboardButton(text="2", callback_data="2"),
            InlineKeyboardButton(text="3", callback_data="3"),
            InlineKeyboardButton(text="4", callback_data="4"),
            InlineKeyboardButton(text="5", callback_data="5"),
        ],
        [
            InlineKeyboardButton(text="6", callback_data="6"),
            InlineKeyboardButton(text="7", callback_data="7"),
            InlineKeyboardButton(text="8", callback_data="8"),
            InlineKeyboardButton(text="9", callback_data="9"),
            InlineKeyboardButton(text="10", callback_data="10")
        ],
        [
            InlineKeyboardButton(text="⬅️", callback_data="ong"),
            InlineKeyboardButton(text="➡️", callback_data="chap")
        ],
        [
            InlineKeyboardButton(text="🔍 Mahsulot Qidirish!", callback_data="search")
        ],
        [
            InlineKeyboardButton(text="🆔 ID Orqali Mahsulot Sotib Olish!", callback_data="id_buy_product")
        ]
    ]
)

async def like_button(score):
    likes = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"❤️ {score}", callback_data="heart")
            ],
            [
                InlineKeyboardButton(text="🛒 Sotib Olish", callback_data="buy")
            ],
            [
                InlineKeyboardButton(text="🏘 Asosiy Menyu", callback_data="main")
            ]
        ]
    )
    return likes

search_product_id = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🆔 ID Orqali Mahsulot Sotib Olish!", callback_data="id_buy_product")
        ]
    ]
)

search_product_id_buys = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🆔 ID Boyicha Mahsulot Ma'lumot Olish", callback_data="id_search_buys")
        ]
    ]
)

update_delate = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛠 Mahsulotni Togirlash", callback_data="set_product"),
        ],
        [
            InlineKeyboardButton(text="❌ Mahsulotni Ochirib Tashlash", callback_data="del_product")
        ],
        [
            InlineKeyboardButton(text="❌ Mahsulotni Bozordan Olib Tashlash", callback_data="del_bozor_product")
        ]
    ]
)

seting = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✍️ Mahsulot Nomini Ozgartirish", callback_data="set_name")
        ],
        [
            InlineKeyboardButton(text="💰 Mahsulot Narxini O'zgartirish", callback_data="set_price")
        ],
        [
            InlineKeyboardButton(text="🖨 Mahsulot Haqida Ma'lumot O'zgartirish", callback_data="set_desc")
        ],
        [
            InlineKeyboardButton(text="🖼 Mahsulot Rasmini O'zgartirish", callback_data="set_photo")
        ],
        [
            InlineKeyboardButton(text="🏘 Asosiy Menyu", callback_data="main")
        ]
    ]
)
