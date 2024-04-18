from aiogram import Router, F
from utils.functions import insert_user_data, check_exist_user_name, check_user_data, \
    check_latynka, check_lat_num, select_all_fuel_type, get_available_liters_by_id, insert_fuel_purchase_data, \
    total_fuel_price, select_all_goods_type, get_available_quantity_by_id, insert_goods_purchase_data, \
    total_goods_price, check_employee_id, add_quantity, check_double, change_goods_price, add_liters, change_fuel_price
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import StartStatus, Registration, Login, Employee, UserStatus, FuelBought, GoodsBought, \
    EmployeeStatus, GoodsChoose, FuelChoose
from keyboards.reply import main, user, bought, rkr, employee, choose_operation, choose_num

router = Router()

user_data = {}
employee_identifier = ""


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Вас вітає телеграм-бот АЗС.\r\n \
    Для початку роботи, вам необхідно зареєструватися,\r\n \
    або увійти в систему з існуючим акаунтом.", reply_markup=main)
    await state.set_state(StartStatus.choose)


@router.message(StartStatus.choose)
async def main_menu(message: Message, state: FSMContext):
    user_data.clear()
    msg = message.text.lower()
    if msg == "зареєструватися":
        await state.clear()
        await message.answer(
            "Придумайте ім'я користувача (логін). За допомогою нього вас можна буде ідентифікувати в системі.\r\n"
            "Дотримуйтеся правил:\r\n"
            "1) Латинські літери\r\n"
            "2) Перший символ - буква алфавіту\r\n"
            "3) Не більше 15 символів", reply_markup=rkr)
        await state.set_state(Registration.login)
    elif msg == "увійти":
        await state.clear()
        await message.answer("Введіть логін:")
        await state.set_state(Login.login)
    elif msg == "я співробітник":
        await state.clear()
        await message.answer("Введіть ідентифікаційний код:")
        await state.set_state(Employee.identifier)
    else:
        await message.answer("Невідома команда", reply_markup=main)


@router.message(Registration.login)
async def login_input(message: Message, state: FSMContext):
    if len(message.text) <= 15 and check_latynka(message.text[0]):
        await state.update_data(login=message.text)
        temp = await state.get_data()
        if check_exist_user_name(temp):
            await state.update_data(login=message.text)
            await message.answer(f"Ваше ім'я: {message.text}. Перейдемо далі.")
            await message.answer(
                "Придумайте пароль\r\n"
                "Дотримуйтеся правил:\r\n"
                "1) Допускаються виключно цифри та латинські літери\r\n"
                "1) Не менше п'яти символів\r\n"
                "2) Не більше двадцяти символів")
            await state.set_state(Registration.password)
        else:
            await message.answer("Користувач з таким іменем вже існує")
    else:
        await message.answer("Невірний формат вводу. Спробуйте ще раз.")


@router.message(Registration.password)
async def password_input(message: Message, state: FSMContext):
    if 5 <= len(message.text) <= 20 and check_lat_num(message.text):
        await state.update_data(password=message.text)
        await message.answer(f"Ваш пароль: {message.text}. Перейдемо далі.")
        await message.answer(
            "Введіть свій ПІБ у форматі: Прізвище Ім'я По-батькові\r\n"
            "Дотримуйтеся правил:\r\n"
            "1) Не більше тридцяти п'яти символів")
        await state.set_state(Registration.full_name)
    else:
        await message.answer("Невірний формат вводу. Спробуйте ще раз.")


@router.message(Registration.full_name)
async def full_name_input(message: Message, state: FSMContext):
    if 5 <= len(message.text) <= 35:
        await state.update_data(full_name=message.text)
        await message.answer(f"Ваш ПІБ: {message.text}. Перейдемо далі.")
        await message.answer(
            "Введіть свій номер телефону (за бажанням) у форматі десяти цифр\r\n"
            "Приклад: (0999999999) \r\n"
            "Щоб пропустити цей пункт, введіть \"пропустити\"")
        await state.set_state(Registration.number)
    else:
        await message.answer("Невірний формат вводу. Спробуйте ще раз.")


@router.message(Registration.number, F.text.casefold() == "пропустити".lower())
async def number_none_input(message: Message, state: FSMContext):
    await state.update_data(number='')
    await message.answer(f"Ваш номер: не вказано. Перейдемо далі.")
    await message.answer(
        "Введіть свою електронну пошту телефону (за бажанням)\r\n"
        "Дотримуйтеся правил:\r\n"
        "1) Довжина не більше 25 символів\r\n"
        "Щоб пропустити цей пункт, введіть \"пропустити\"")
    await state.set_state(Registration.e_mail)


@router.message(Registration.number)
async def number_input(message: Message, state: FSMContext):
    if message.text.isdigit() and len(message.text) == 10:
        await state.update_data(number=message.text)
        await message.answer(f"Ваш номер: {message.text}. Перейдемо далі.")
        await message.answer(
            "Введіть свою електронну пошту телефону (за бажанням)\r\n"
            "Дотримуйтеся правил:\r\n"
            "1) Довжина не більше 25 символів\r\n"
            "Щоб пропустити цей пункт, введіть \"пропустити\"")
        await state.set_state(Registration.e_mail)
    else:
        await message.answer("Невірний формат вводу. Спробуйте ще раз.")


@router.message(Registration.e_mail, F.text.casefold() == "пропустити".lower())
async def e_mail_none_input(message: Message, state: FSMContext):
    await state.update_data(e_mail='')
    await message.answer(f"Ваша електронна пошта: не вказано. Перейдемо далі.")
    await message.answer("Ви успішно зареєструвалися!", reply_markup=main)
    data = await state.get_data()
    insert_user_data(data)
    await state.clear()
    await state.set_state(StartStatus.choose)


@router.message(Registration.e_mail)
async def e_mail_input(message: Message, state: FSMContext):
    await state.update_data(e_mail=message.text)
    await message.answer(f"Ваша електронна пошта: {message.text}. Перейдемо далі.")
    await message.answer("Ви успішно зареєструвалися!", reply_markup=main)
    data = await state.get_data()
    insert_user_data(data)
    await state.clear()
    await state.set_state(StartStatus.choose)


@router.message(Login.login)
async def login_exist_input(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введіть пароль")
    await state.set_state(Login.password)


@router.message(Login.password)
async def login_exist_input(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    if check_user_data(data):
        await message.answer("Ви увійшли в акаунт!")
        global user_data
        user_data = data.copy()
        await state.clear()
        await message.answer("Оберіть одну з доступних опцій", reply_markup=user)
        await state.set_state(UserStatus.choose)
    else:
        await message.answer("Користувача не знайдено...")
        await state.clear()
        await message.answer("Вас вітає телеграм-бот АЗС.\r\n \
            Для початку роботи, вам необхідно зареєструватися,\r\n \
            або увійти в систему з існуючим акаунтом.", reply_markup=main)
        await state.set_state(StartStatus.choose)


@router.message(UserStatus.choose, F.text.casefold() == "купити пальне".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer(select_all_fuel_type())
    await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
    await state.set_state(FuelBought.fuel)


@router.message(UserStatus.choose, F.text.casefold() == "купити товари".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer(select_all_goods_type())
    await message.answer('Виберіть товари, які ви хочете придбати.', reply_markup=bought)
    await state.set_state(GoodsBought.goods)


@router.message(UserStatus.choose, F.text.casefold() == "вийти".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Вас вітає телеграм-бот АЗС.\r\n \
        Для початку роботи, вам необхідно зареєструватися,\r\n \
        або увійти в систему з існуючим акаунтом.", reply_markup=main)
    await state.set_state(StartStatus.choose)


@router.message(UserStatus.choose)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=user)


@router.message(FuelBought.fuel)
async def echo(message: Message, state: FSMContext):
    msg = message.text.lower()
    if msg == "1":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel1)
    elif msg == "2":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel2)
    elif msg == "3":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel3)
    elif msg == "4":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel4)
    elif msg == "5":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel5)
    elif msg == "6":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel6)
    elif msg == "7":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel7)
    elif msg == "8":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel8)
    elif msg == "9":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel9)
    elif msg == "10":
        await message.answer("Введіть кількість літрів", reply_markup=rkr)
        await state.set_state(FuelBought.fuel10)
    elif msg == "скасувати":
        await message.answer("Операція відхилена")
        await state.clear()
        await state.set_state(UserStatus.choose)
        await message.answer("Оберіть одну з доступних опцій", reply_markup=user)
    elif msg == "готово":
        data = await state.get_data()
        await state.clear()
        insert_fuel_purchase_data(data, user_data)
        await state.set_state(UserStatus.choose)
        await message.answer(f"Загальна сума складає {total_fuel_price(data)} грн.", reply_markup=user)
        await message.answer("Оберіть одну з доступних опцій")
    else:
        await message.answer("Невідома команда", reply_markup=bought)


@router.message(FuelBought.fuel1)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(1) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel1=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(FuelBought.fuel2)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(2) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel2=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(FuelBought.fuel3)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(3) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel3=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(FuelBought.fuel4)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(4) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel4=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(FuelBought.fuel5)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(5) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel5=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(FuelBought.fuel6)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(6) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel6=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(FuelBought.fuel7)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(7) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel7=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(FuelBought.fuel8)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(8) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel8=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(FuelBought.fuel9)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(9) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel9=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(FuelBought.fuel10)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_liters_by_id(10) < int(msg):
            await message.answer("Недостатньо пального в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(fuel10=msg)
            await message.answer('Виберіть пальне, яке ви хочете придбати.', reply_markup=bought)
            await state.set_state(FuelBought.fuel)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods)
async def echo(message: Message, state: FSMContext):
    msg = message.text.lower()
    if msg == "1":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods1)
    elif msg == "2":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods2)
    elif msg == "3":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods3)
    elif msg == "4":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods4)
    elif msg == "5":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods5)
    elif msg == "6":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods6)
    elif msg == "7":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods7)
    elif msg == "8":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods8)
    elif msg == "9":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods9)
    elif msg == "10":
        await message.answer("Введіть кількість", reply_markup=rkr)
        await state.set_state(GoodsBought.goods10)
    elif msg == "скасувати":
        await message.answer("Операція відхилена")
        await state.clear()
        await state.set_state(UserStatus.choose)
        await message.answer("Оберіть одну з доступних опцій", reply_markup=user)
    elif msg == "готово":
        data = await state.get_data()
        await state.clear()
        insert_goods_purchase_data(data, user_data)
        await state.set_state(UserStatus.choose)
        await message.answer(f"Загальна сума складає {total_goods_price(data)} грн.", reply_markup=user)
        await message.answer("Оберіть одну з доступних опцій")
    else:
        await message.answer("Невідома команда", reply_markup=bought)


@router.message(GoodsBought.goods1)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(1) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods1=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods2)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(2) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods2=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods3)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(3) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods3=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods4)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(4) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods4=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods5)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(5) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods5=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods6)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(6) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods6=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods7)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(7) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods7=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods8)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(8) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods8=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods9)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(9) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods9=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(GoodsBought.goods10)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        if get_available_quantity_by_id(10) < int(msg):
            await message.answer("Недостатньо товару в наявності")
        else:
            await message.answer("Додано")
            await state.update_data(goods10=msg)
            await message.answer('Виберіть товар, який ви хочете придбати.', reply_markup=bought)
            await state.set_state(GoodsBought.goods)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз")


@router.message(Employee.identifier)
async def identify(message: Message, state: FSMContext):
    if check_employee_id(message.text):
        global employee_identifier
        employee_identifier = message.text
        await message.answer("Оберіть одну з доступних опцій", reply_markup=employee)
        await state.set_state(EmployeeStatus.choose)
    else:
        await state.set_state(StartStatus.choose)
        await message.answer("Працівника з таким ідентифікатором не знайдено", reply_markup=main)


@router.message(EmployeeStatus.choose)
async def choose_option(message: Message, state: FSMContext):
    msg = message.text.lower()
    if msg == "таблиця пального":
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    elif msg == "таблиця товарів":
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    elif msg == "вийти":
        await message.answer("Вас вітає телеграм-бот АЗС.\r\n \
                Для початку роботи, вам необхідно зареєструватися,\r\n \
                або увійти в систему з існуючим акаунтом.", reply_markup=main)
        await state.set_state(StartStatus.choose)
    else:
        await message.answer("Некоректні дані. Спробуйте ще раз", reply_markup=employee)


@router.message(EmployeeStatus.choose_product)
async def echo(message: Message, state: FSMContext):
    msg = message.text.lower()
    if msg == "1":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods1)
    elif msg == "2":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods2)
    elif msg == "3":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods3)
    elif msg == "4":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods4)
    elif msg == "5":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods5)
    elif msg == "6":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods6)
    elif msg == "7":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods7)
    elif msg == "8":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods8)
    elif msg == "9":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods9)
    elif msg == "10":
        await message.answer("Що ви хочете зробити з товаром?", reply_markup=choose_operation)
        await state.set_state(GoodsChoose.goods10)
    elif msg == "Готово".lower():
        await message.answer("Оберіть одну з доступних опцій", reply_markup=employee)
        await state.set_state(EmployeeStatus.choose)
    else:
        await message.answer("Невідома команда", reply_markup=choose_num)


@router.message(GoodsChoose.goods1, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_1)


@router.message(GoodsChoose.add_quan_1)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=1)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods1, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_1)


@router.message(GoodsChoose.change_price_1)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=1)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods1)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(GoodsChoose.goods2, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_2)


@router.message(GoodsChoose.add_quan_2)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=2)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods2, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_2)


@router.message(GoodsChoose.change_price_2)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=2)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods2)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(GoodsChoose.goods3, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_3)


@router.message(GoodsChoose.add_quan_3)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=3)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods3, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_3)


@router.message(GoodsChoose.change_price_3)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=3)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods3)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(GoodsChoose.goods4, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_4)


@router.message(GoodsChoose.add_quan_4)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=4)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods4, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_4)


@router.message(GoodsChoose.change_price_4)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=4)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods4)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(GoodsChoose.goods5, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_5)


@router.message(GoodsChoose.add_quan_5)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=5)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods5, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_5)


@router.message(GoodsChoose.change_price_5)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=5)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods5)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(GoodsChoose.goods6, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_6)


@router.message(GoodsChoose.add_quan_6)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=6)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods6, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_6)


@router.message(GoodsChoose.change_price_6)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=6)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods6)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(GoodsChoose.goods7, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_7)


@router.message(GoodsChoose.add_quan_7)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=7)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods7, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_7)


@router.message(GoodsChoose.change_price_7)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=7)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods7)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(GoodsChoose.goods8, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_8)


@router.message(GoodsChoose.add_quan_8)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=8)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods8, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_8)


@router.message(GoodsChoose.change_price_8)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=8)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods8)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(GoodsChoose.goods9, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_9)


@router.message(GoodsChoose.add_quan_9)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=9)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods9, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_9)


@router.message(GoodsChoose.change_price_9)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=9)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods9)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(GoodsChoose.goods10, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(GoodsChoose.add_quan_10)


@router.message(GoodsChoose.add_quan_10)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(goods_id=10)
        await state.update_data(goods_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_quantity(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods10, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(GoodsChoose.change_price_10)


@router.message(GoodsChoose.change_price_10)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(goods_id=10)
        await state.update_data(goods_price=float(msg))
        data = await state.get_data()
        change_goods_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_product)
        await message.answer(select_all_goods_type())
        await message.answer('Виберіть товар, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(GoodsChoose.goods10)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(EmployeeStatus.choose_fuel)
async def echo(message: Message, state: FSMContext):
    msg = message.text.lower()
    if msg == "1":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel1)
    elif msg == "2":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel2)
    elif msg == "3":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel3)
    elif msg == "4":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel4)
    elif msg == "5":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel5)
    elif msg == "6":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel6)
    elif msg == "7":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel7)
    elif msg == "8":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel8)
    elif msg == "9":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel9)
    elif msg == "10":
        await message.answer("Що ви хочете зробити з пальним?", reply_markup=choose_operation)
        await state.set_state(FuelChoose.fuel10)
    elif msg == "Готово".lower():
        await message.answer("Оберіть одну з доступних опцій", reply_markup=employee)
        await state.set_state(EmployeeStatus.choose)
    else:
        await message.answer("Невідома команда", reply_markup=choose_num)


@router.message(FuelChoose.fuel1, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_1)


@router.message(FuelChoose.add_liters_1)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=1)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel1, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_1)


@router.message(FuelChoose.change_price_1)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=1)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel1)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(FuelChoose.fuel2, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_2)


@router.message(FuelChoose.add_liters_2)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=2)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel2, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_2)


@router.message(FuelChoose.change_price_2)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=2)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel2)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(FuelChoose.fuel3, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_3)


@router.message(FuelChoose.add_liters_3)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=3)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel3, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_3)


@router.message(FuelChoose.change_price_3)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=3)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel3)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(FuelChoose.fuel4, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_4)


@router.message(FuelChoose.add_liters_4)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=4)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel4, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_4)


@router.message(FuelChoose.change_price_4)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=4)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel4)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(FuelChoose.fuel5, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_5)


@router.message(FuelChoose.add_liters_5)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=5)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel5, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_5)


@router.message(FuelChoose.change_price_5)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=5)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel5)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(FuelChoose.fuel6, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_6)


@router.message(FuelChoose.add_liters_6)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=6)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel6, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_6)


@router.message(FuelChoose.change_price_6)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=6)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel6)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(FuelChoose.fuel7, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_7)


@router.message(FuelChoose.add_liters_7)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=7)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel7, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_7)


@router.message(FuelChoose.change_price_7)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=7)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel7)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(FuelChoose.fuel8, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_8)


@router.message(FuelChoose.add_liters_8)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=8)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel8, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_8)


@router.message(FuelChoose.change_price_8)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=8)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel8)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(FuelChoose.fuel9, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_9)


@router.message(FuelChoose.add_liters_9)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=9)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel9, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_9)


@router.message(FuelChoose.change_price_9)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=9)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel9)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message(FuelChoose.fuel10, F.text.casefold() == "змінити кількість".lower())
async def change_quantity(message: Message, state: FSMContext):
    await message.answer("Вкажіть кількість, яку ви хочете додати до наявної кількості.")
    await state.set_state(FuelChoose.add_liters_10)


@router.message(FuelChoose.add_liters_10)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        await state.update_data(fuel_id=10)
        await state.update_data(liters_quantity=int(msg))
        await state.update_data(identifier=employee_identifier)
        data = await state.get_data()
        add_liters(data)
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel10, F.text.casefold() == "змінити ціну".lower())
async def echo(message: Message, state: FSMContext):
    await message.answer("Введіть нову ціну.")
    await message.answer("(До двох значень після крапки)")
    await state.set_state(FuelChoose.change_price_10)


@router.message(FuelChoose.change_price_10)
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if check_double(msg):
        await state.update_data(fuel_id=10)
        await state.update_data(fuel_price=float(msg))
        data = await state.get_data()
        change_fuel_price(data)
        await message.answer("Зміни внесено!")
        await state.clear()
        await state.set_state(EmployeeStatus.choose_fuel)
        await message.answer(select_all_fuel_type())
        await message.answer('Виберіть пальне, у якому ви хочете внести зміни.', reply_markup=choose_num)
    else:
        await message.answer("Невірний формат вводу")


@router.message(FuelChoose.fuel10)
async def echo(message: Message):
    await message.answer("Невідома команда", reply_markup=choose_operation)


@router.message()
async def echo(message: Message):
    await message.answer("Я не розумію команди")
