from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeywordsCallbackFactory(CallbackData, prefix="keyword"):
    action: Literal["add", "delete"]


keywords_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Добавить ключевое слово',
                                 callback_data=KeywordsCallbackFactory(action='add').pack()),
            InlineKeyboardButton(text='Удалить ключевое слово',
                                 callback_data=KeywordsCallbackFactory(action='delete').pack())
        ]
    ]
)
