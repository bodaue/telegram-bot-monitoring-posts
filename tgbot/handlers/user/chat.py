import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import i18n

from tgbot.db.db_api import chats
from tgbot.misc.states import ChannelState
from tgbot.my_types.user import User

chat_router = Router()


@chat_router.message(F.text.in_(('Список моих каналов', '/my_channels')))
async def get_my_chats(message: Message):
    user_id = message.from_user.id
    user = User(user_id=user_id)
    text = await user.format_chats_text()
    await message.answer(text=text)


@chat_router.message(F.text.in_(('Добавить канал', '/add_channel')))
async def chat_add(message: Message, state: FSMContext):
    await message.answer('<b>Отправьте ссылку на канал.</b>\n\n'
                         '<b>Возможные форматы:</b>\n'
                         '@channelname\n'
                         't.me/channelname\n'
                         'channelname')

    await state.set_state(ChannelState.waiting_add)


@chat_router.message(ChannelState.waiting_add)
async def waiting_chat_add(message: Message, state: FSMContext):
    await state.clear()

    user_id = message.from_user.id
    user = User(user_id=user_id)
    count_subs = await user.count_chats()
    if count_subs >= 10:
        await message.answer('<b>Вы не можете добавить более 10 каналов</b>')
        return

    chat_link = message.text.lower().strip()
    chat_link = re.sub(r'@|https:|t\.me|/', '', chat_link)

    chat = await chats.find_one({'username': chat_link})
    if chat:
        chat_id = chat.get('_id')
        if await user.has_chat(chat_id=chat_id):
            await message.answer('<b>Этот канал уже есть в Вашем списке каналов</b>')
            return

        await user.add_chat(chat_id=chat_id)

        await message.answer(f'<b>Канал успешно добавлен в список Ваших каналов</b>\n\n'
                             f'<b>Название:</b> {chat["title"]}\n'
                             f'<b>Ссылка:</b> @{chat_link}')
        return

    #  если канала нет в базе
    # for app_join in apps_join:
    #     try:
    #         await app_join.join_chat(chat_id=chat_link)
    #         chat = await app_join.get_chat(chat_id=chat_link)
    #
    #     except ChannelsTooMuch:
    #         continue
    #
    #     except Exception as ex:
    #         print(ex, '1')
    #         await message.answer('<b>Не удалось найти такой канал</b>')
    #
    #     else:
    #         title = chat.title
    #         chat_id = chat.id
    #         description = chat.description
    #         members_count = chat.members_count
    #         if chat.photo:
    #             photo_id = chat.photo.big_file_id
    #             photo = f'django_project/media/chat_images/{chat_link}.jpg'
    #             photo_path = f'chat_images/{chat_link}.jpg'
    #             await app_join.download_media(photo_id, file_name=photo)
    #         else:
    #             photo_path = None
    #
    #         await chats.insert_one({'_id': chat_id,
    #                                 'username': chat_link,
    #                                 'title': title,
    #                                 'photo': photo_path,
    #                                 'description': description,
    #                                 'count_subscribers': members_count,
    #                                 'status': True,
    #                                 'date': date,
    #                                 'get_messages': False})
    #
    #         await users_chats.insert_one({'_id': str(uuid.uuid4()),
    #                                       'user_id': user_id,
    #                                       'chat_id': chat_id,
    #                                       'date': date})
    #
    #         await message.answer(f'<b>Канал успешно добавлен в список Ваших каналов</b>\n\n'
    #                              f'<b>Название:</b> {title}\n'
    #                              f'<b>Ссылка:</b> @{chat_link}')


@chat_router.message(F.text.in_(('Удалить канал', '/delete_channel')))
async def chat_delete(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = User(user_id=user_id)
    count_subs = await user.count_chats()

    if count_subs == 0:
        await message.answer('<b>Список каналов пуст</b>')
        return

    await message.answer('<b>Для удаления отправьте ссылку на канал.</b>\n\n'
                         '<b>Возможные форматы:</b>\n'
                         '@channelname\n'
                         't.me/channelname\n'
                         'channelname')

    await state.set_state(ChannelState.waiting_delete)


@chat_router.message(ChannelState.waiting_delete)
async def waiting_chat_delete(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    chat_link = message.text.lower().strip()
    chat_link = re.sub(r'@|https:|t\.me|/', '', chat_link)
    chat = await chats.find_one({'username': chat_link})
    if not chat:
        return await message.answer('Такого канала нет')

    chat_id = chat.get('_id')

    user = User(user_id=user_id)
    if await user.has_chat(chat_id=chat_id):
        await user.delete_chat(chat_id=chat_id)
        await message.answer(f'<b>Вы успешно удалили канал @{chat_link} из списка Ваших каналов</b>\n\n'
                             f'<b>Теперь Вам не будут приходить уведомления от этого канала</b>')

    else:
        await message.answer('<b>Этого канала нет в списке Ваших каналов</b>')
