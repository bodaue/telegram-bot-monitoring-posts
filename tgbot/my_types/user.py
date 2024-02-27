from datetime import datetime

from pymongo.errors import DuplicateKeyError

from tgbot.db.db_api import users
from tgbot.my_types.user_chats import UserChatsMixin
from tgbot.my_types.user_keywords import UserKeywordsMixin


class User(UserKeywordsMixin, UserChatsMixin):
    _collection = users

    @classmethod
    async def create(cls,
                     user_id: int,
                     name: str,
                     username: str):
        try:
            await cls._collection.insert_one(
                {'_id': user_id,
                 'name': name,
                 'username': username,
                 'date': datetime.now()})
        except DuplicateKeyError:
            await cls.update(self=cls(user_id=user_id),
                             name=name,
                             username=username)
        return cls(user_id=user_id)

    async def get_data(self):
        return await self._collection.find_one({'_id': self.user_id})

    async def update(self, **kwargs):
        await self._collection.update_one(filter={'_id': self.user_id},
                                          update={'$set': kwargs})
