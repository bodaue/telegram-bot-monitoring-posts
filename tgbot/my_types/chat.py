from contextlib import suppress

from pymongo.errors import DuplicateKeyError

from tgbot.db.db_api import chats


class Chat:
    _collection = chats

    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    @classmethod
    async def create(cls,
                     chat_id: int,
                     title: str,
                     link: str):
        with suppress(DuplicateKeyError):
            await cls._collection.insert_one({'_id': chat_id,
                                              'title': title,
                                              'link': link})
        return cls(chat_id=chat_id)

    async def get_data(self):
        return await self._collection.find_one({'_id': self.chat_id})
