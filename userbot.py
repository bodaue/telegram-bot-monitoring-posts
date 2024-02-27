import asyncio

from pyrogram import Client, compose, filters
from pyrogram.handlers import MessageHandler, EditedMessageHandler, DeletedMessagesHandler

from bot import register_logger
from userbot.filter import chat_filter
from userbot.handlers.add_message import add_new_message
from userbot.handlers.change_message import edited_message
from userbot.handlers.delete_message import deleted_message


async def get_clients() -> list[Client]:
    return [
        Client(api_id=2040, api_hash='b18441a1ff607e10a989891a5462e627', name='userbot/sessions/account_1'),
        Client(api_id=2040, api_hash='b18441a1ff607e10a989891a5462e627', name='userbot/sessions/account_2')
    ]


def register_handlers(apps: list[Client]):
    for app in apps:
        app.add_handler(MessageHandler(add_new_message, chat_filter & (filters.text | filters.caption)))
        app.add_handler(EditedMessageHandler(edited_message, chat_filter & (filters.text | filters.caption)))
        app.add_handler(DeletedMessagesHandler(deleted_message, chat_filter))


async def main():
    apps = await get_clients()

    register_handlers(apps)
    await compose(apps)


if __name__ == '__main__':
    register_logger()

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
