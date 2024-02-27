from aiogram import html

from tgbot.db.db_api import users_keywords


class UserKeywordsMixin:

    def __init__(self, user_id: int):
        self.user_id = user_id

    async def count_keywords(self) -> int:
        return await users_keywords.count_documents({'user_id': self.user_id})

    async def get_keywords(self) -> list[dict]:
        cursor = users_keywords.find({'user_id': self.user_id})
        user_keywords = await cursor.to_list(length=None)
        return user_keywords

    async def format_keywords_text(self) -> str:
        keywords = await self.get_keywords()
        if not keywords:
            return html.bold('Список ключевых слов пуст.')

        text = html.bold('Ваши ключевые слова\n\n')

        for index, keyword in enumerate(keywords):
            word = keyword['text']
            text += html.bold(f'{index + 1}. {html.quote(word)}\n')

        return text

    async def has_keyword(self, keyword: str) -> bool:
        return await users_keywords.find_one({'user_id': self.user_id,
                                              'text': {'$regex': f'^(?i){keyword}$'}})

    async def add_keyword(self, keyword: str) -> None:
        await users_keywords.insert_one({'user_id': self.user_id,
                                         'text': keyword})

    async def delete_keyword(self, keyword: str) -> None:
        await users_keywords.delete_one({'user_id': self.user_id,
                                         'text': {'$regex': f'^(?i){keyword}$'}})
