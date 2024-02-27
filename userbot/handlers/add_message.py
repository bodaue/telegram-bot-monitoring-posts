import logging
import re
from datetime import datetime

from aiogram import html
from aiogram.types import FSInputFile
from pyrogram import types

from tgbot.db.db_api import chat_posts, users, users_keywords, chats
from userbot.utils import get_word_cases


async def add_new_message(_, message: types.Message):
    text = message.text if message.text else message.caption
    chat_id = message.chat.id
    repost_from_chat_id = None
    if message.forward_from_chat:
        repost_from_chat_id = message.forward_from_chat.id
    elif message.forward_from:
        repost_from_chat_id = message.forward_from.id

    logging.info(f'Новое сообщение из группы {chat_id} (Link: {message.link}) - {text}')

    if message.photo:
        photo_path = f'images/{chat_id}/{message.id}_1.jpg'
        photo = f'django_project/media/{photo_path}'
        await message.download(file_name=photo)
    else:
        photo_path = None
        photo = None

    if message.video and chat_id == 'workbrothers':
        video_path = f'videos/{chat_id}/{message.id}.mp4'
        video = f'django_project/media/{video_path}'
        await message.download(file_name=video)
    else:
        video_path = None

    date = message.date
    await chat_posts.insert_one(
        {'chat_id': chat_id,
         'message_id': message.id,
         'text': text,
         'date': date,
         'photo': photo_path,
         'video': video_path,
         'repost_from_chat_id': repost_from_chat_id})

    time = datetime.today().replace(hour=0, minute=0, second=0)
    count_posts = await chat_posts.count_documents({'chat_id': chat_id})
    count_posts_today = await chat_posts.count_documents({'date': {'$gte': time}, 'chat_id': chat_id})

    await chats.update_one(filter={'_id': chat_id},
                           update={'$set': {'count_posts': count_posts, 'count_posts_today': count_posts_today}})

    # for delay in range(60, 721, 60):
    #     get_views.apply_async(args=(group_id, message.message_id, _id, date, delay),
    #                           countdown=delay * 60)
    chat_link = html.link(value=message.chat.title,
                          link=f't.me/{message.chat.username}')

    async for user in users.find():
        found = []
        user_id = user['_id']
        async for keyword in users_keywords.find({'user_id': user_id}):
            key = keyword['text']
            forms = get_word_cases(key)
            for form in set(forms):
                if re.search(re.escape(form), text, re.IGNORECASE):
                    found.append(form)

        if found:
            text_to_send = text
            for word in found:
                text_to_send = re.sub(pattern=word,
                                      repl=f'<u><b>{word}</b></u>',
                                      string=text_to_send,
                                      flags=re.IGNORECASE)

            found = list(map(quotes, found))
            text_to_send = (f'В канале <b>{chat_link}</b> были использованы ключевые слова: {", ".join(found)}\n\n'
                            f''
                            f'<b>Текст</b>:\n'
                            f'{text_to_send}\n\n'
                            f'{message.link}')
            try:
                if message.photo:
                    photo = FSInputFile(photo)
                    await dp.bot.send_photo(chat_id=user_id,
                                            photo=photo,
                                            caption=text_to_send[:1024])
                else:
                    await dp.bot.send_message(chat_id=user_id,
                                              text=text_to_send[:4096])
            except:
                continue


def quotes(word: str) -> str:
    return f'«{word}»'
