import logging
from datetime import datetime

from pyrogram.types import Message

from tgbot.db.db_api import chats, chat_posts


async def deleted_message(_, messages: list[Message]):
    date = datetime.now()
    for message in messages:
        message_id = message.id
        chat_id = message.chat.id
        chat = await chats.find_one({'_id': chat_id})
        title = chat.get('title')
        logging.info(f'Удалено сообщение в группе {title} (Link: {message.link})')

        await chat_posts.update_one(filter={'chat_id': chat_id,
                                            'message_id': message_id},
                                    update={'is_deleted': True,
                                            'deleted_at': date},
                                    upsert=True)

#         all_posts = posts.find({'group_id': group_id, 'message_id': message_id}).sort('date', 1)
#         first_post = posts.find_one({'group_id': group_id, 'message_id': message_id, 'type': 'new_post'})
#         for user in subs.find({'group_id': group_id}):
#             try:
#                 await bot.send_message(chat_id=user['user_id'], text='<b>_________________________________</b>')
#                 await bot.send_message(chat_id=user['user_id'],
#                                        text=f'''<b>Новое изменение!</b>
# <b>Название группы:</b>{name_group}
# <b>Ссылка на группу:</b> @{group_id}
# <b>ID сообщения:</b> {message_id}
#
# История изменений:''')
#             except:
#                 pass
#         for post in all_posts:
#             text = post['text']
#             date_change = post['date']
#             type_of_change = types_changes[post['type']]
#
#             if first_post and post['type'] != 'new_post':
#                 delta = (date_change - first_post['date'])
#                 delta = delta - timedelta(microseconds=delta.microseconds)
#                 delta = f"<b>Времени с публикации оригинала:</b>" \
#                         f" {delta}\n"
#             else:
#                 delta = ''
#             date_change = date_change.strftime("%d.%m.%Y %H:%M:%S")
#             photo = post['photo']
#             if photo:
#                 photo = f'django_project/media/{photo}'
#                 try:
#                     photo = InputFile(path_or_bytesio=photo)
#                 except FileNotFoundError:
#                     photo = None
#             if post['type'] == 'deleted':
#                 msg = f'<b>Дата: </b>{date_change}\n' \
#                       f'{delta}' \
#                       f'<b>Тип:</b> {type_of_change}\n\n'
#             else:
#                 msg = f'<b>Дата: </b>{date_change}\n' \
#                       f'{delta}' \
#                       f'<b>Тип:</b> {type_of_change}\n\n' \
#                       f'<b>Текст:</b>\n{text}\n\n'
#
#             for user in subs.find({'group_id': group_id}):
#                 try:
#                     if photo:
#                         await bot.send_photo(chat_id=user["user_id"], caption=msg, photo=photo,
#                                              disable_notification=True)
#                     else:
#                         await bot.send_message(chat_id=user["user_id"], text=msg, disable_web_page_preview=True)
#                 except Exception as e:
#                     print(e, 'qwe')
#
#         time = datetime.today().replace(hour=0, minute=0, second=0)
#         always_count = posts.count_documents({'group_id': group_id})
#         today_count = posts.count_documents({'date': {'$gte': time}, 'group_id': group_id})
#
#         groups.update_one({'group_id': group_id},
#                           {'$set': {'always_count': always_count, 'today_count': today_count}})
