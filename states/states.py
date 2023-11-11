from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStates(StatesGroup):
    full_name = State()
    phone_number = State()
    login = State()
    password = State()

class Add_Product(StatesGroup):
    product_name = State()
    product_photo = State()
    product_price = State()
    how_it_worked = State()

class WriteAdmin(StatesGroup):
    write = State()

class SaleProduct(StatesGroup):
    select_num = State()
    acept = State()

class SearchProduct(StatesGroup):
    search = State()

class SearchProuct_id(StatesGroup):
    id_search = State()

class IdSearch(StatesGroup):
    id_searchch = State()