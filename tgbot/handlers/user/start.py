from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from tgbot.handlers.user.chat import chat_router
from tgbot.handlers.user.keywords import keywords_router
from tgbot.keyboards.reply import main_markup

user_router = Router()
user_router.include_routers(keywords_router,
                            chat_router)

user_router.message.filter(F.chat.type == "private")
user_router.callback_query.filter(F.message.chat.type == 'private')


@user_router.message(CommandStart())
async def bot_start(message: Message):
    await message.answer(f'<b>Привет, {message.from_user.full_name}!\n'
                         f'Используй клавиатуру для работы с ботом ⬇</b>',
                         reply_markup=main_markup)
