from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Мои чаты'),
        KeyboardButton(text='Мои ключевые слова')
    ]
],
    resize_keyboard=True)
