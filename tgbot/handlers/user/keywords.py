from aiogram import Router, F, html, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType, CallbackQuery

from tgbot.keyboards.inline import keywords_keyboard, KeywordsCallbackFactory
from tgbot.misc.states import KeywordState
from tgbot.my_types.user import User

keywords_router = Router()


@keywords_router.message(F.text == 'Мои ключевые слова')
async def get_my_keywords(message: Message):
    user_id = message.from_user.id
    user = User(user_id=user_id)

    text = await user.format_keywords_text()
    await message.answer(text=text,
                         reply_markup=keywords_keyboard)


@keywords_router.callback_query(KeywordsCallbackFactory.filter(F.action == 'add'))
async def add_keyword(call: CallbackQuery, state: FSMContext):
    await call.answer('Отправьте ключевое слово')

    message_id = call.message.message_id
    await state.set_state(KeywordState.waiting_add)
    await state.update_data(message_id=message_id)


@keywords_router.message(KeywordState.waiting_add, F.text)
async def waiting_keyword_add(message: Message, state: FSMContext, bot: Bot):
    keyword = message.text.strip()
    user_id = message.from_user.id
    user = User(user_id=user_id)
    if await user.has_keyword(keyword=keyword):
        await message.answer(html.bold('Ключевое слово уже добавлено.'))
    else:
        await message.answer(html.bold('Ключевое слово добавлено'))
        await user.add_keyword(keyword)

        state_data = await state.get_data()
        message_id = state_data.get('message_id')
        text = await user.format_keywords_text()
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=message_id,
                                    text=text,
                                    reply_markup=keywords_keyboard)
    await state.clear()


@keywords_router.message(KeywordState.waiting_add)
async def bad_waiting_keyword_to_add(message: Message):
    await message.answer('Ожидается текст')


@keywords_router.callback_query(KeywordsCallbackFactory.filter(F.action == 'delete'))
async def delete_keyword(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user = User(user_id=user_id)
    if await user.count_keywords() == 0:
        return await call.answer('Список ключевых слов пуст')

    await call.answer('Отправьте ключевое слово')

    message_id = call.message.message_id
    await state.set_state(KeywordState.waiting_delete)
    await state.update_data(message_id=message_id)


@keywords_router.message(KeywordState.waiting_delete, F.content_type == ContentType.TEXT)
async def waiting_keyword_delete(message: Message, state: FSMContext, bot: Bot):
    keyword = message.text.strip()
    user_id = message.from_user.id
    user = User(user_id=user_id)
    if await user.has_keyword(keyword=keyword):
        await message.answer(html.bold('Ключевое слово удалено.'))
        await user.delete_keyword(keyword=keyword)

        state_data = await state.get_data()
        message_id = state_data.get('message_id')
        text = await user.format_keywords_text()
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=message_id,
                                    text=text,
                                    reply_markup=keywords_keyboard)
    else:
        await message.answer(html.bold('Такого ключевого слова нет в Вашем списке'))

    await state.clear()


@keywords_router.message(KeywordState.waiting_delete)
async def bad_waiting_keyword_to_delete(message: Message):
    await message.answer('Ожидается текст')
