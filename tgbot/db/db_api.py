from motor.motor_asyncio import AsyncIOMotorClient

from tgbot.config import config

client = AsyncIOMotorClient(host=config.db.host,
                            port=config.db.port)

db = client[config.db.name]

#  инициализируем коллекции
users = db['users']
users_keywords = db['users_keywords']

chats = db['chats']
users_chats = db['users_chats']

chat_posts = db['chat_posts']
edited_chat_posts = db['edited_chat_posts']

chat_posts_views = db['chat_posts_views']

settings = db['settings']

keywords = db['keywords']
posts_keywords = db['posts_keywords']

tgstat_statistic = db['tgstat_statistic']
