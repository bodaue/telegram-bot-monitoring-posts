from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, html
from aiogram.types import Message

from tgbot.config import config
from tgbot.db.db_api import users
from tgbot.keyboards.reply import main_markup
from tgbot.my_types.user import User


class AuthorizationMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:

        user_id = event.from_user.id
        username = event.from_user.username
        name = event.from_user.full_name

        user = await users.find_one(filter={'_id': user_id})
        if user:
            return await handler(event, data)

        text = event.text if event.text else event.caption
        if text and text == config.tg_bot.password:
            await User.create(user_id=user_id,
                              username=username,
                              name=name)
            await event.answer(text=html.bold('Вы успешно авторизовались!'),
                               reply_markup=main_markup)
        else:
            await event.answer(html.bold('Введите парольную фразу для взаимодействия с ботом'))
