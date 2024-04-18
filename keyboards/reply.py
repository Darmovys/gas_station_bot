from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Зареєструватися"),
            KeyboardButton(text="Увійти")
        ],
        [
            KeyboardButton(text="Я співробітник"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Виберіть дію з меню",
)

user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Купити пальне"),
            KeyboardButton(text="Купити товари")
        ],
        [
            KeyboardButton(text="Вийти"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Виберіть дію з меню",
)

bought = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4"),
        ],
        [
            KeyboardButton(text="5"),
            KeyboardButton(text="6"),
            KeyboardButton(text="7"),
            KeyboardButton(text="8"),
        ],
        [
            KeyboardButton(text="9"),
            KeyboardButton(text="10"),
            KeyboardButton(text="Готово"),
            KeyboardButton(text="Скасувати")
        ]
    ],
    resize_keyboard=True
)

rkr = ReplyKeyboardRemove()

employee = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Таблиця пального"),
            KeyboardButton(text="Таблиця товарів")
        ],
        [
            KeyboardButton(text="Вийти"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Виберіть дію з меню",
)


choose_operation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Змінити кількість"),
            KeyboardButton(text="Змінити ціну")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Виберіть дію з меню",
)

choose_num = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4"),
        ],
        [
            KeyboardButton(text="5"),
            KeyboardButton(text="6"),
            KeyboardButton(text="7"),
            KeyboardButton(text="8"),
        ],
        [
            KeyboardButton(text="9"),
            KeyboardButton(text="10"),
            KeyboardButton(text="Готово"),
        ]
    ],
    resize_keyboard=True
)
