from pyrogram import filters
from pyrogram.types import Message

from tgbot.db.db_api import chats


def func_from_chat(_, __, message: Message):
    chat_id = message.chat.id
    return await chats.find_one({'_id': chat_id})


# def func_from_chat_id(_, __, query):
#     all_groups = [i['chat_id'] for i in groups.find({'status': 'добавлен'})]
#     if query.chat.id:
#         return query.chat.id in all_groups
#     return False


# def func_check_changes(_, __, message: Message):
#     message_id = message.id
#     chat_id = message.chat.id
#     last_post = posts.find_one({'chat_id': chat_id,
#                                 'message_id': message_id})
#     try:
#         last_post = list(posts.find({'group_id': username, 'message_id': message_id}))[-1]
#     except:
#         return True
#     if not username:
#         return False
#     return last_post['text'] != text


# filter_check_changes = filters.create(func_check_changes)
chat_filter = filters.create(func_from_chat)

# filter_chat_id = filters.create(func_from_chat_id)
