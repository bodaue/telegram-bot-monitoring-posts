import logging
from datetime import datetime, timedelta

from aiogram.types import InputFile
from pyrogram.types import Message

from tgbot.db.db_api import edited_chat_posts, chats, users_chats
from userbot.utils import check_difference

types_changes = {'edited': 'изменение поста', 'new_post': 'добавление поста', 'deleted': 'удаление поста'}


async def edited_message(_, message: Message):
    text = message.text if message.text else message.caption

    message_id = message.id
    date = message.edit_date
    chat_id = message.chat.id

    logging.info(f'Изменено сообщение в группе {chat_id} (Link: {message.link}) - {text}')

    count_posts = await edited_chat_posts.count_documents({'chat_id': chat_id,
                                                      'message_id': message_id}) + 2

    if message.photo:
        photo_path = f'images/{chat_id}/{message.id}_{count_posts}.jpg'
        photo = f'django_project/media/{photo_path}'
        await message.download(file_name=photo)
    else:
        photo_path = None

    # if message.video and group_id == 'workbrothers':
    #     video = f'django_project/media/videos/{group_id}/{message.message_id}.mp4'
    #     video_path = f'videos/{group_id}/{message.message_id}.mp4'
    #     await message.download(file_name=video)
    # else:
    #     video_path = None
    video_path = None
    chat = await chats.find_one({'_id': chat_id})
    title = chat.get('title')
    try:
        last_post = list(edited_posts.find({'chat_id': chat_id, 'message_id': message_id}))[-1]['text']
    except:
        last_post = ''

    await edited_posts.insert_one({'chat_id': chat_id,
                                   'message_id': message_id,
                                   'text': text,
                                   'date': date,
                                   'photo': photo_path,
                                   'video': video_path})

    all_posts = posts.find({'group_id': group_id, 'message_id': message_id}).sort('date', 1)
    first_post = posts.find_one({'group_id': group_id, 'message_id': message_id, 'type': 'new_post'})

    for user in users_chats.find({'chat_id': chat_id}):
        try:
            await dp.bot.send_message(chat_id=user['user_id'], text='<b>_________________________________</b>')
            await dp.bot.send_message(chat_id=user['user_id'],
                                      text=f'''<b>Новое изменение!</b>
<b>Название группы:</b>{name_group}
<b>Ссылка на группу:</b> @{group_id}
<b>ID сообщения:</b> {message_id}

История изменений:''')
        except Exception as e:
            print(e, 'qweqwe')
            pass

    for index, post in enumerate(all_posts):
        text = post['text']
        date_change = post['date']
        type_of_change = types_changes[post['type']]

        if first_post and post['type'] != 'new_post':
            delta = (date_change - first_post['date'])
            delta = delta - timedelta(microseconds=delta.microseconds)
            delta = f"<b>Времени с публикации оригинала:</b>" \
                    f" {delta}\n"
        else:
            delta = ''

        date_change = date_change.strftime('%d.%m.%Y %H:%M:%S')
        photo = post['photo']
        if photo:
            photo = f'django_project/media/{photo}'
            try:
                photo = InputFile(path_or_bytesio=photo)
            except FileNotFoundError:
                photo = None
        if last_post and text_msg:
            if count_posts - index == 2:
                text = check_difference(last_post, str(text_msg))[0]
            elif count_posts - index == 1:
                text = check_difference(last_post, str(text_msg))[1]

        msg = f'<b>Дата: </b>{date_change}\n' \
              f'{delta}' \
              f'<b>Тип:</b> {type_of_change}\n\n' \
              f'<b>Текст:</b>\n' \
              f'{text}\n\n' \
              f'{message.link}'

        for user in subs.find({'group_id': group_id}):
            try:
                if photo:
                    print(msg, 'photo')
                    await dp.bot.send_photo(chat_id=user["user_id"], caption=msg[:1024], photo=photo)
                else:
                    print(msg, 'text')
                    await dp.bot.send_message(chat_id=user["user_id"], text=msg[:4096],
                                              disable_web_page_preview=True)
            except Exception as e:
                print(e, 'qweqdwqe')

    today = datetime.today().replace(hour=0, minute=0, second=0)
    always_count = posts.count_documents({'group_id': group_id})
    today_count = posts.count_documents({'date': {'$gte': today}, 'group_id': group_id})

    groups.update_one({'group_id': group_id}, {'$set': {'always_count': always_count, 'today_count': today_count}})
