from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    login = State()
    password = State()
    full_name = State()
    number = State()
    e_mail = State()


class Login(StatesGroup):
    login = State()
    password = State()


class Employee(StatesGroup):
    identifier = State()


class StartStatus(StatesGroup):
    choose = State()


class UserStatus(StatesGroup):
    choose = State()
    choose_product = State()
    choose_fuel = State()


class FuelBought(StatesGroup):
    fuel = State()
    fuel1 = State()
    fuel2 = State()
    fuel3 = State()
    fuel4 = State()
    fuel5 = State()
    fuel6 = State()
    fuel7 = State()
    fuel8 = State()
    fuel9 = State()
    fuel10 = State()


class GoodsBought(StatesGroup):
    goods = State()
    goods1 = State()
    goods2 = State()
    goods3 = State()
    goods4 = State()
    goods5 = State()
    goods6 = State()
    goods7 = State()
    goods8 = State()
    goods9 = State()
    goods10 = State()


class EmployeeStatus(StatesGroup):
    choose = State()
    choose_product = State()
    choose_fuel = State()


class FuelChoose(StatesGroup):
    fuel1 = State()
    add_liters_1 = State()
    change_price_1 = State()
    fuel2 = State()
    add_liters_2 = State()
    change_price_2 = State()
    fuel3 = State()
    add_liters_3 = State()
    change_price_3 = State()
    fuel4 = State()
    add_liters_4 = State()
    change_price_4 = State()
    fuel5 = State()
    add_liters_5 = State()
    change_price_5 = State()
    fuel6 = State()
    add_liters_6 = State()
    change_price_6 = State()
    fuel7 = State()
    add_liters_7 = State()
    change_price_7 = State()
    fuel8 = State()
    add_liters_8 = State()
    change_price_8 = State()
    fuel9 = State()
    add_liters_9 = State()
    change_price_9 = State()
    fuel10 = State()
    add_liters_10 = State()
    change_price_10 = State()


class GoodsChoose(StatesGroup):
    goods1 = State()
    add_quan_1 = State()
    change_price_1 = State()
    goods2 = State()
    add_quan_2 = State()
    change_price_2 = State()
    goods3 = State()
    add_quan_3 = State()
    change_price_3 = State()
    goods4 = State()
    add_quan_4 = State()
    change_price_4 = State()
    goods5 = State()
    add_quan_5 = State()
    change_price_5 = State()
    goods6 = State()
    add_quan_6 = State()
    change_price_6 = State()
    goods7 = State()
    add_quan_7 = State()
    change_price_7 = State()
    goods8 = State()
    add_quan_8 = State()
    change_price_8 = State()
    goods9 = State()
    add_quan_9 = State()
    change_price_9 = State()
    goods10 = State()
    add_quan_10 = State()
    change_price_10 = State()
