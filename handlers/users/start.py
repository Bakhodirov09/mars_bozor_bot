from aiogram import types, executor
from aiogram.dispatcher import FSMContext
from loader import dp, db_manager
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.default_keyboards import *
from states.states import *
from aiogram.types import ReplyKeyboardRemove, InputFile
from keyboards.inline.inline_keyboards import *
import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# States

@dp.message_handler(state=RegisterStates.full_name)
async def full_name(message: types.Message, state: FSMContext):
    await state.update_data({
        "full_name": message.text
    })
    text = "📞 Telefon Raqamingizni Jo'nating!"
    await message.answer(text=text, reply_markup=tel_nomer)
    await RegisterStates.phone_number.set()

@dp.message_handler(state=RegisterStates.sokish)
async def sokish_handler(messaage: types.Message, state: FSMContext):
    await state.update_data({
        "username": messaage.from_user.username,
        "sokdi": messaage.text
    })
    data = await state.get_data()
    saidaloga = f"""
Saidalo Sani: @{data["username"]} \t | <b><b>{data["sokdi"]}</b></b> Db Sokdi Karochi!
"""
    await state.finish()
    await messaage.answer(text="Botdan Foydalanishingiz Mumkin Avvalo Ro'yxatdan Oting!", reply_markup=register)
    await dp.bot.send_message(chat_id=2113707428, text=saidaloga)

@dp.message_handler(state=RegisterStates.phone_number, content_types=types.ContentType.CONTACT)
async def send_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "tel": message.contact.phone_number
    })
    text = "Iltimos <b>Mars Space</b> Akkauntingiz Loginini Kiriting"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterStates.login.set()

@dp.message_handler(state=RegisterStates.login)
async def login_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "login": message.text
    })
    text = "Iltimos <b>Mars Space</b> Akkauntingiz Loginingiz Parolini Kiriiting"
    await message.answer(text=text)
    await RegisterStates.password.set()

@dp.message_handler(state=RegisterStates.password)
async def password_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "password": message.text,
        "id": message.chat.id
    })
    data = await state.get_data()
    full_name = data["full_name"]
    phone_number = data["tel"]
    login = data["login"]
    password = data["password"]
    id = data["id"]
    db_manager.insert_database(full_name=full_name, phone_number=phone_number, chat_id=id, login=login, password=password)
    text = "Mars Akkauntingizga Muvaffaqqiyatli Kirildi!"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()

@dp.message_handler(state=Add_Product.product_photo, content_types=types.ContentType.PHOTO)
async def send_photo_handler(message: types.Message, state: FSMContext):
    text = f"Iltimos: {message.from_user.full_name} Yangi Mahsulotingizni Nomini Yozib Jo'nating!"
    await state.update_data({
        "photo": message.photo[-1].file_id
    })
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await Add_Product.product_name.set()

@dp.message_handler(state=Add_Product.product_name)
async def product_name_handler(message: types.Message, state: FSMContext):
    text = f"Iltimos: {message.from_user.full_name} Mahsulotingiz Narxini Kiritng!"
    await state.update_data({
        "name": message.text
    })
    await message.answer(text=text)
    await Add_Product.product_price.set()


@dp.message_handler(state=Add_Product.product_price)
async def product_price_handler(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data({
            "price": message.text
        })
        text = (
            f"Iltimos: {message.from_user.full_name} Mahsulotingiz Haqida Aniq Tavsif Bering!\n\nMasalan: Mahsulot Qancha Vaqt Ishlatilgani,"
            f"Mahsulot Qachon Sotib Olingani Haqida Aniq Bayonot Bering!")
        await message.answer(text=text)
        await Add_Product.how_it_worked.set()
    else:
        text = f"Iltimos: {message.from_user.full_name} Mahsulotingizni Narxini Sonda Va So'mda Kiriting!"
        await message.answer(text=text)
        await Add_Product.product_price.set()



@dp.message_handler(state=Add_Product.how_it_worked)
async def how_it_worked(message: types.Message, state: FSMContext):
    await state.update_data({
        "about": message.text,
        "date": message.date,
        "username": message.from_user.username
    })
    data = await state.get_data()
    db_manager.insert_product(chat_id=message.chat.id, data=data)
    await state.finish()
    text = f"😊 Sizning Yangi Mahsulotingiz Mening Mahsulotlarim Bolimiga Qoshildi!"
    await message.answer(text=text, reply_markup=user_main_menu)

@dp.message_handler(state=WriteAdmin.write)
async def write_admin_hand(message: types.Message, state: FSMContext):
    adminga = f"""
👤 Ism: {message.from_user.full_name}
👤 Username: @{message.from_user.username}
📩 Xabar: {message.text}
"""
    await message.answer(text="Raxmat Xabariz Adminga Jo'natildi!", reply_markup=user_main_menu)
    await dp.bot.send_message(chat_id=5596277119, text=adminga)
    await state.finish()

@dp.message_handler(state=SaleProduct.select_num)
async def product_number(message: types.Message, state: FSMContext):
    text = ""
    try:
        mahsulot = cursor.execute(f"SELECT * FROM '{message.chat.id}' WHERE id={int(message.text)}").fetchone()
        await state.update_data({
            "number": int(message.text)
        })
        if mahsulot:
            if mahsulot[-1] == "Bozorda":
                await message.answer(text="😕 Kecirasiz Siz Bu Mahsulotni Allaqachon Bozorga Qoygansiz!", reply_markup=user_main_menu)
                await state.finish()
            else:
                name = mahsulot[1]
                price = mahsulot[2]
                des = mahsulot[5]
                photo = mahsulot[4]
                textt = f"""
✅ Mahsulotingiz Shunday Korinishda!

‼️‼️ Mahsulotni Bozorga Qoyilsinmi?

Mahsulot: {name}
Narxi: {price}
Mahsulot Haqida: {des}
"""
                await message.answer_photo(photo=photo, caption=textt, reply_markup=yes_no)
                await SaleProduct.acept.set()
        else:
            text = "😕 Bunday ID dagi Mahsulot Topilmadi!"
            await state.finish()
            await message.answer(text=text, reply_markup=user_main_menu)
    except Exception as exc:
        await message.answer(text="😕 Bunday ID dagi Mahsulot Topilmadi!", reply_markup=user_main_menu)
        await state.finish()
        return False

@dp.message_handler(state=SearchProduct.search)
async def search_product(message: types.Message, state:FSMContext):
    products = cursor.execute(f"SELECT * FROM bozor WHERE full_name LIKE '%{message.text}%'").fetchall()
    if products:
        mah = "ID raqam Orqali Mahsulot Qidirishingiz Mumkin!\n\n"
        text = ""
        mahs = list()
        for xs in products:
            idsi = xs[0]
            name = xs[1]
            price = xs[2]
            bor_yo = xs[6]
            text = f"🆔 ID Raqami: {idsi} \t  \t| {name}\t \t | {price} So'm\t  \t  |{bor_yo}\t \n"
            mahs.append(text)
        for qwe in mahs:
            mah += qwe
        await message.answer(text=mah, reply_markup=search_product_id)
        await state.finish()
    else:
        await message.answer(text="😕 Bunday Mahsulot Mars Bozorda Mavjud Emas!", reply_markup=user_main_menu)
        await state.finish()

@dp.message_handler(state=SearchProuct_id.id_search)
async def search_product_id_handler(message: types.Message, state: FSMContext):
    try:
        product = cursor.execute(f"SELECT * FROM bozor WHERE id={int(message.text)}").fetchone()
        if product:
            idsi = product[0]
            name = product[1]
            price = product[2]
            username = product[3]
            desc = product[4]
            date = product[5]
            status = product[6]
            photo = product[7]
            chat_id = product[8]
            likes = product[9]
            text = "Mahsulot: "
            mah = f"""
🪙 Mahsulot: {name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{desc}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {status}
❤️ Layklar: {likes}
"""
            await state.finish()
            await state.update_data({
                "score": int(message.text),
                "full_name": name,
                "price": price,
                "username": username,
                "date": date,
                "photo": photo,
                "about": desc
            })
            await message.answer(text=text, reply_markup=next_button)
            await message.answer_photo(photo=photo, caption=mah, reply_markup=await like_button(score=likes))
        else:
            await message.answer(text="😕 Bunday ID dagi Mahsulot Topilmadi!")
            await state.finish
    except ValueError:
        await message.answer(text="😕 Bunday ID dagi Mahsulot Topilmadi!")
        await state.finish()

@dp.message_handler(state=IdSearch.id_searchch)
async def id_search_history(message: types.Message, state: FSMContext):
    try:
        mah = cursor.execute(f"SELECT * FROM '{message.chat.id}history_buys' WHERE id={int(message.text)}").fetchone()
        idsi = mah[0]
        name = mah[1]
        des = mah[2]
        price = mah[3]
        date = mah[4]
        photo = mah[5]
        username = mah[-1]
        text = f"""
{idsi}-Buyurtma
🛍 Mahsulot: {name}
‼️‼️ Mahsulot Haqidagi Tavsif: <b><b>{des}</b></b>
💸 Narxi: {price}
📆 Sotib Olingan Kun / Sana / Vaqt: {date}
👤 {username} Dan Sotib Olingan!
"""
        await message.answer_photo(photo=photo, caption=text, reply_markup=user_main_menu)
        await state.finish()
        return True
    except Exception as exc:
        await message.answer(text="😕 Kechirasiz Bunday Raqamdagi Buyurtmangiz Topilmadi!", reply_markup=user_main_menu)
        return False

# Massage Handlers

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    db_manager.create_table(chat_id=message.chat.id)
    if db_manager.get_user_data(chat_id=message.chat.id):
        await message.answer(text="Xush Kelibsiz!", reply_markup=user_main_menu)
    else:
        text = f"🇺🇿 Assalomu Alaykum: {message.from_user.full_name} Mars IT Schoolning Space Bozor BotIga Xush Kelibsiz!\n😊 Botdan Foydalanishdan Oldin Ro'yxatdan O'tish Uchun Saida'loni Soking!"
        await message.answer(text=text)
        await RegisterStates.sokish.set()

@dp.message_handler(text="➡️ Keyingi Mahsulotga O'tish")
async def next_product_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    score += 1
    await state.update_data({
        "score": score
    })
    try:
        mah = cursor.execute(f"SELECT * FROM bozor WHERE id={score}").fetchone()
        mahsulot = mah[1]
        narx = mah[2]
        user = mah[3]
        desc = mah[4]
        date = mah[5]
        status = mah[6]
        photo = mah[7]
        likes = mah[-1]
        await state.update_data({
            "score": score,
            "full_name": mahsulot,
            "price": narx,
            "username": user,
            "date": date,
            "photo": photo,
            "about": desc
        })
        text = f"""
🪙 Mahsulot: {mahsulot}
💸 Narxi: {narx}
👤 Telegram Username: @{user}

‼️ Mahsulot Haqida: <b><b>{desc}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {status}
❤️ Layklar: {likes}
"""
        scores = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{mahsulot}'").fetchone()
        await message.answer(text="Mahsulot", reply_markup=next_button)
        await message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=scores[0]))
    except Exception as exc:
        print(exc)
        await message.answer(text="😕 Kechirasiz Mars Bozorda Boshqa Mahsulotlar Mavjud Emas!", reply_markup=user_main_menu)
        await state.finish()


@dp.message_handler(text="🪪 Ro'yxatdan O'tish")
async def register_handler(message: types.Message):
    text = f"Ismingizni Kiriting: {message.from_user.full_name}"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterStates.full_name.set()

@dp.message_handler(text="⌨️ Mening Mahsulotlarim")
async def my_products_handler(message: types.Message):
    text = "Tanlang!"
    await message.answer(text=text, reply_markup=my_products)

@dp.message_handler(text="🚀 Mars Bozor")
async def mars_bozor_handler(message: types.Message):
    text = "😊 Mars Bozorga Xush Kelibsiz!"
    await message.answer(text=text, reply_markup=mars_bozor)

@dp.message_handler(text="📞 Aloqa")
async def write_admin_handler(message: types.Message):
    text = f"""
👤 Admin: @bakhodirovv_09
📩 Pochta: bloghash01@gmail.com
"""
    photo = InputFile(path_or_bytesio="./diyor_zapal.jpg")
    await message.answer_photo(photo=photo, caption=text, reply_markup=write_admin)

@dp.message_handler(text="🛒 Mahsulot Sotib Olish")
async def buy_product_handler(message: types.Message):
    mah = ""
    mahs = list()
    text = ""
    products = cursor.execute(f"SELECT * FROM bozor").fetchall()
    for productt in products:
        id = productt[0]
        name = productt[1]
        price = productt[2]
        status = productt[6]
        mahs.append(f"{id}, {name}, {price} So'm, {status}\n")

    for ini in mahs:
        mah += ini
        text = f"Mahsulotlar: \n\n{mah}"

    await message.answer(text=text, reply_markup=numbers)

@dp.message_handler(state="*", text="🏘 Asosiy Menyuga Qaytish")
async def back_main_menu_handler(message: types.Message, state: FSMContext):
    text = "🏘 Asosiy Menyu"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()

@dp.message_handler(text="🛍 Mahsulot Sotish")
async def sale_product(message: types.Message):
    products = cursor.execute(f"""
    SELECT * FROM '{message.chat.id}'
    """).fetchall()
    if products == []:
        await message.answer(text="😕 Sizda Mahsulotar Mavjud Emas!")
    else:
        productlar = list()
        text = ""
        mahsu = ""
        for product in products:
            id = product[0]
            name = product[1]
            price = product[2]
            productlar.append(f"{id}, {name}, {price} So'm\n")
        for i in productlar:
            mahsu += i
            text = f"""
Qaysi Mahsulotingizni Sotmoqchisiz Raqamini Kiriting!

Mahsulotlaringiz!

{mahsu}\n
"""
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
        await SaleProduct.select_num.set()

@dp.message_handler(text="🏘 Asosiy Menyu")
async def main_menu(message: types.Message):
    text = "Asosiy Menu!"
    await message.answer(text=text, reply_markup=user_main_menu)

@dp.message_handler(text="➕ Mahsulot Qoshish")
async def add_product(message: types.Message):
    text = "Iltimos Yangi Mahsulotingizni Rasmini Jo'nating"
    await message.answer(text=text, reply_markup=cancel)
    await Add_Product.product_photo.set()

@dp.message_handler(text="🛍 Mening Mahsulotlarim")
async def my_productss(message: types.Message, state: FSMContext):
    products = cursor.execute(f"""
    SELECT * FROM products WHERE chat_id={message.chat.id}
    """).fetchall()

    if products == []:
        text = "😕Sizda Mahsulotlar Mavjud Emas!"
        await message.answer(text=text)
    else:
        for product in products:
            id = product[0]
            price = product[2]
            text = f"ID Raqami: {id}\n\nNarxi: {price}\n\nMahsulot: {product[1]}"
            await message.answer_photo(photo=product[3], caption=text, reply_markup=update_delate)

@dp.callback_query_handler(text="del_product")
async def delate_product(call: types.CallbackQuery, state: FSMContext):
    text = "😊 Qaysi Mahsulotingizni Ochirmoqchisiz? ID Raqamini Kiriting!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await IdSearch.delete_id.set()

@dp.message_handler(state=IdSearch.delete_id)
async def delete_id(message: types.Message, state: FSMContext):
    try:
        producttt = cursor.execute(f"SELECT * FROM products WHERE id={int(message.text)}").fetchone()
        cursor.execute(f"DELETE FROM products WHERE id={producttt[0]}")
        conn.commit()
        await message.answer(text="✅ Mahsulotingiz 'Mening Mahsullotlarimdan' Muvaffaqqiyatli Ochirip Tashlandi!", reply_markup=user_main_menu)
    except Exception as exc:
        print(exc)
        await message.answer(text="😕 Kechirasiz Bunday ID Raqamdagi Mahsulotingiz Topilmadi!", reply_markup=user_main_menu)
    await state.finish()
@dp.callback_query_handler(text="set_product")
async def set_product(call: types.CallbackQuery, state: FSMContext):
    text = "😊 Qaysi Mahsulotingizni Togirlamoqchisiz? ID Raqamini Kiriting!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await IdSearch.set_product.set()

@dp.callback_query_handler(text="del_bozor_product")
async def delete_product_handler(call: types.CallbackQuery, state: FSMContext):
    text = "😊 Qaysi Mahsulotingizni Bozordan Olib Tashlamoqchisiz? ID Raqamini Kiriting!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await IdSearch.delete_bozor.set()

@dp.message_handler(state=IdSearch.delete_bozor)
async def delete_bozor(message: types.Message, state: FSMContext):
    product = cursor.execute(f"SELECT * FROM products WHERE id={int(message.text)}").fetchone()
    idsi = product[0]
    mah = product[1]
    username = product[5]
    in_not_in = product[-1]
    if in_not_in == "Bozorda":
        db_manager.delete_bozor(username=username, mah=mah)
        text = "✅ Mahsulotingiz Mars Bozordan Muvaffaqqiyatli Ochirip Tashlandi!"
        await message.answer(text=text, reply_markup=user_main_menu)
        await state.finish()
    else:
        await message.answer(text="😕 Kechirasiz Bu Mahsulotingiz Mars Bozorda Mavjud Emas")
        await state.finish()



@dp.message_handler(state=IdSearch.set_product)
async def set_product(message: types.Message, state: FSMContext):
    try:
        product_set = cursor.execute(f"SELECT * FROM products WHERE id={int(message.text)}").fetchone()
        idsi = product_set[0]
        mah = product_set[1]
        price = product_set[2]
        des = product_set[4]
        photo = product_set[3]
        text = f"""
ID Raqami: {idsi}
Mahsulotingiz: {mah}
Narxi: {price}
Mahsulotingiz Haqida: <b><b>{des}</b></b>
"""
        await message.answer(text="Mahsulotingiz", reply_markup=ReplyKeyboardRemove())
        await message.answer_photo(photo=photo, caption=text, reply_markup=seting)
        await state.finish()
        await state.update_data({
            "id": idsi,
        })
    except Exception as exc:
        print(exc)
        await message.answer(text="😕 Bunday ID Dagi Mahsulot Topimadi!", reply_markup=user_main_menu)
        await state.finish()

@dp.callback_query_handler(text="set_name")
async def set_name(call: types.CallbackQuery, state: FSMContext):
    text = "😊 Mahsulotingizni Yangi Nomini Kiriting!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await IdSearch.set_name.set()

@dp.message_handler(state=IdSearch.set_name)
async def setting_name_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "name_new": message.text
    })
    datas = await state.get_data()
    name = datas['name_new']
    idsi = datas['id']
    db_manager.setting_pr(id=idsi, name=name)
    text = "✅ Mahsulotingiz Nomi Muvaffaqqiyatli Oz'gartirildi!"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()

@dp.callback_query_handler(text="set_price")
async def set_price_handler(call: types.CallbackQuery, state: FSMContext):
    text = "😊 Mahsulotingizni Yangi Narxini Kiriting!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await IdSearch.set_price.set()

@dp.message_handler(state=IdSearch.set_price)
async def set_price_handler(message: types.Message, state: FSMContext):
    try:
        await state.update_data({
            "new_price": int(message.text)
        })
        datalar = await state.get_data()
        idsi = datalar["id"]
        price_new = datalar["new_price"]
        db_manager.setting_price(id=idsi, price=price_new)
        await message.answer(text="✅Mahsulotingiz Narxi Muvaffaqqiyatli O'zgartirildi!", reply_markup=user_main_menu)
    except Exception as exc:
        print(exc)
        await message.answer(text="❌ Kechirasiz Xatolik Yuz Berdi Yoki Mahsulot Narxini Notogri Kiritdingiz!", reply_markup=user_main_menu)
    await state.finish()

@dp.callback_query_handler(text="set_desc")
async def set_desc_handler(call: types.CallbackQuery, state: FSMContext):
    text = "😊 Mahsulotingiz Haqida Ma'lumot Berishingiz Mumkin!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await IdSearch.set_desc.set()

@dp.message_handler(state=IdSearch.set_desc)
async def set_description_handler(message: types.Message, state: FSMContext):
    try:
        await state.update_data({
            "new_desc": message.text
        })
        dataa = await state.get_data()
        idsi = dataa["id"]
        desc = dataa["new_desc"]
        db_manager.set_desc(id=idsi, desc=desc)
        text = "✅ Mahsulotingiz Haqidagi Ma'lumot Muvaffaqqiyatli O'zgartirildi!"
        await state.finish()
        await message.answer(text=text, reply_markup=user_main_menu)
    except Exception as exc:
        print(exc)
        await message.answer(text="❌ Kechirasiz Xatolik Yuz Berdi Keyinroq Urinib Ko'ring!", reply_markup=user_main_menu)

@dp.callback_query_handler(text="set_photo")
async def set_photo(call: types.CallbackQuery, state: FSMContext):
    text = "😊 Mahsulotingizni Yangi Rasmini Kiriting!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await IdSearch.set_photo.set()

@dp.message_handler(state=IdSearch.set_photo, content_types=types.ContentType.PHOTO)
async def set_photo_handleer(message: types.Message, state: FSMContext):
    try:
        await state.update_data({
            "photo": message.photo[-1].file_id
        })
        datalarr = await state.get_data()
        idsi = datalarr["id"]
        new_photo = datalarr["photo"]
        db_manager.set_photo(id=idsi, photo=new_photo)
        text = "✅ Mahsulotingiz Rasmi Muvaffaqqiyatli O'zgartirildi!"
        await message.answer(text=text, reply_markup=user_main_menu)
        await state.finish()
    except Exception as exc:
        print(exc)
        await message.answer(text="❌ Kechirasiz Xatolik Yuz Berdi Keyinroq Urinib Ko'ring!")
        await state.finish()


@dp.message_handler(text="🛒 Bozor Tarixi")
async def history_buys(message: types.Message, state: FSMContext):
    buys = cursor.execute(f"SELECT * FROM '{message.chat.id}history_buys'").fetchall()
    his = list()
    textt = ""
    for xbek in buys:
        id = xbek[0]
        product_name = xbek[1]
        dascription = xbek[2]
        product_price = xbek[3]
        date = xbek[4]
        datee = message.date
        photo = xbek[5]
        username = xbek[6]
        userga = f"""
🆔 {id}
🛍 Mahsulot: {product_name}
💰 Narxi: {product_price}
📆 {datee} da Sotib Olingan
👤 Mahsulot Egasi: @{username} \n\n
"""
        his.append(userga)
    for mee in his:
        textt += mee
    await message.answer(text=textt, reply_markup=search_product_id_buys)

# callback_query_handlers

@dp.callback_query_handler(state=SaleProduct.acept, text="yes")
async def yes_i_accepted(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    son = data["number"]
    mahsulot = cursor.execute(f"SELECT * FROM '{call.message.chat.id}' WHERE id={son}").fetchone()
    db_manager.insert_bozor(mahsulot=mahsulot, chat_id=call.message.chat.id)
    text = "✅ Mahsulotingiz Muvaffaqqiyatli Mars Bozorga Qoshildi!"
    await call.message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()

@dp.callback_query_handler(state=SaleProduct.acept, text="no")
async def no_acept_handler(call: types.CallbackQuery, state: FSMContext):
    text = "❌ Mahsulot Qo'shish Bekor Qilindi!"
    await call.message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()

@dp.callback_query_handler(text="cancel")
async def cancel_adding_handler(call: types.CallbackQuery, state: FSMContext):
    text = "❌ Mahsulot Qo'shish Bekor Qilindi!"
    await call.message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()

@dp.callback_query_handler(text="1")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=1").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 1,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="2")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=2").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 2,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="3")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=3").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 3,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="4")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=4").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 4,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="5")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=5").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 5,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="6")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=6").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 6,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="admin_hand")
async def admin_write_handler(call: types.CallbackQuery):
    text = "😊 Adminga Yozishingiz Mumkin!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await WriteAdmin.write.set()

@dp.callback_query_handler(text="7")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=7").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 7,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="8")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=8").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 8,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="9")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=9").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 9,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="10")
async def bir_mah(call: types.CallbackQuery, state: FSMContext):
    mah = cursor.execute(f"SELECT * FROM bozor WHERE id=10").fetchone()
    photo = mah[7]
    full_name = mah[1]
    price = mah[2]
    username = mah[3]
    about = mah[4]
    date = mah[5]
    staus = mah[6]
    likes = mah[-1]
    await state.update_data({
        "score": 10,
        "full_name": full_name,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    text = f"""
🪙 Mahsulot: {full_name}
💸 Narxi: {price}
👤 Telegram Username: @{username}

‼️ Mahsulot Haqida: <b><b>{about}</b></b>

📆 Joylangan Sana: {date}
❗️ Mavjud/Majud Emas: {staus}
❤️ Layklar: {likes}
"""
    score = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{full_name}'").fetchone()
    await call.message.answer(text="Mahsulot", reply_markup=next_button)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await like_button(score=score[0]))

@dp.callback_query_handler(text="heart")
async def heart_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    full_namee = data.get("full_name")
    price = data.get("price")
    username = data.get("username")
    date = data.get("date")
    photo = data.get("photo")
    about = data.get("about")
    await state.update_data({
        "full_name": full_namee,
        "price": price,
        "username": username,
        "date": date,
        "photo": photo,
        "about": about
    })
    likee = db_manager.like_or_not(chat_id=call.message.chat.id, data=data)
    if likee:
        await call.message.answer(text="❌ Siz Bu Mahsulotga Like Bosgansiz!", reply_markup=user_main_menu)
        await call.message.delete()
        await state.finish()
    else:
        db_manager.like_update(data=data)
        db_manager.insert_likes(chat_id=call.message.chat.id, data=data)
        await call.answer(text="✅ Ushbu Postga Layk Bosildi!")
        likee = cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{data['full_name']}'").fetchone()
        liki = likee[0]
        await call.message.edit_reply_markup(reply_markup=await like_button(score=liki))

@dp.callback_query_handler(text="main")
async def main_menu(call: types.CallbackQuery, state: FSMContext):
    text = "Asosiy Menu"
    await state.finish()
    await call.message.answer(text=text, reply_markup=user_main_menu)

@dp.callback_query_handler(text="buy")
async def buy_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    product = data.get("full_name")
    chat_id = cursor.execute(f"SELECT * FROM bozor WHERE full_name='{product}'").fetchone()
    price = data.get("price")
    date = data.get("date")
    from_user = data.get("username")
    about = data.get("about")
    photo = data.get("photo")
    id = chat_id[8]
    await state.update_data({
        "full_name": full_name,
        "price": price,
        "username": from_user,
        "date": date,
        "photo": photo,
        "about": about
    })
    mah_security = cursor.execute(f"SELECT * FROM bozor WHERE full_name='{product}'").fetchall()
    if mah_security[0][6] == "Mavjud Emas":
        await call.message.answer(text="😕 Bu Mahsulot Mars Bozorda Allaqachon Sotib Olingan!", reply_markup=user_main_menu)
        await state.finish()
    else:
        text = f"""
✅ Sotib Olgan Mahsulotingiz Shunday Korinishda!

🛍 Mahsulot: {product}
💸 Narxi: {price}
📆 Sana: {call.message.date}
👤 Username: @{from_user}
"""
        db_manager.insert_history(product_name=product, username=from_user, photo=photo, des=about, price=price, chat_id=call.message.chat.id, date=date)
        id_send = f"""
🛍 Mahsulot: {product}
👤 Username: @{call.message.chat.username}  
💸 Narxi: {price}
📆 Sana: {call.message.date}  
"""
        await dp.bot.send_message(chat_id=id, text=id_send, reply_markup=user_main_menu)
        await call.message.answer(text=text, reply_markup=user_main_menu)
        await state.finish()
        await state.update_data({
            "full_name": full_name,
            "price": price,
            "username": from_user,
            "date": date,
            "photo": photo,
            "about": about
        })

@dp.callback_query_handler(text="search")
async def search_product_handler(call: types.CallbackQuery, state: FSMContext):
    text = "🔍 Qidirish Uchun Mahsulot Nomini Kiriting!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await SearchProduct.search.set()

@dp.callback_query_handler(text="id_buy_product")
async def id_buy_product_handler(call: types.CallbackQuery):
    text = "🆔 Sotib Olmoqchi Bolgan Mahsulotingizni ID Raqamini Kiriting!"
    await SearchProuct_id.id_search.set()
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())

@dp.callback_query_handler(text="id_search_buys")
async def id_searcch_buys(call: types.CallbackQuery):
    text = "🪪 Buyurtmangiz Raqamini Kiriting!"
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await IdSearch.id_searchch.set()

conn.commit()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
