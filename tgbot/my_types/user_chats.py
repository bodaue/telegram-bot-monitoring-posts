from datetime import datetime

from aiogram import html

from tgbot.db.db_api import users_chats, chats


class UserChatsMixin:

    def __init__(self, user_id: int):
        self.user_id = user_id

    async def count_chats(self) -> int:
        return await users_chats.count_documents({'user_id': self.user_id})

    async def get_chats(self) -> list[dict]:
        cursor = users_chats.find({'user_id': self.user_id})
        user_chats = await cursor.to_list(length=None)
        return user_chats

    async def format_chats_text(self) -> str:
        user_chats = await self.get_chats()
        if not user_chats:
            return html.bold('Список чатов пуст.')

        text = html.bold('Ваши чаты\n\n')

        for index, chat in enumerate(user_chats):
            chat_id = chat.get('chat_id')

            chat = await chats.find_one({'_id': chat_id})
            title = chat.get('title')

            text += html.bold(f'{index + 1}. {title}\n')

        return text

    async def has_chat(self, chat_id: int) -> bool:
        return await users_chats.find_one({'user_id': self.user_id,
                                           'chat_id': chat_id})

    async def add_chat(self, chat_id: int) -> None:
        await users_chats.insert_one({'user_id': self.user_id,
                                      'chat_id': chat_id,
                                      'date': datetime.now()})

    async def delete_chat(self, chat_id: int) -> None:
        await users_chats.delete_one({'user_id': self.user_id,
                                      'chat_id': chat_id})
