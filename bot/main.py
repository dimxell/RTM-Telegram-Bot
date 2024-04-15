import requests
from io import BytesIO

from configparser import ConfigParser

from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.types import Message

from bot.keyboards import startup_keyboard
from discogsparser.parser import DiscogsAPI


cfg = ConfigParser()
cfg.read('config.conf')

token = cfg.get("Bot", "bot_token")

bot = AsyncTeleBot(token, state_storage=StateMemoryStorage())
discogs_parser = DiscogsAPI(cfg.get("Discogs", "api_token"))

class SearchStates(StatesGroup):
    search_album = State()
    search_release = State()


# Handle '/start'
@bot.message_handler(commands=['start'])
async def send_on_start(message: Message):
    await bot.send_message(message.from_user.id, "Выбери что-то нахуй.", reply_markup=startup_keyboard())



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: message.text == "Поиск по релизу")
async def echo_message(message: Message):
    await bot.send_message(message.from_user.id, "Введи название альбома/релиза")
    await bot.set_state(message.from_user.id, SearchStates.search_release, message.chat.id)

@bot.message_handler(state=SearchStates.search_release)
async def search_release(message: Message):
    releases = discogs_parser.search_release(message.text)

    await bot.send_message(message.from_user.id, "\n".join(f"{r.title} ({r.release_year}) / {r.genres}" for r in releases))
    await bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(func=lambda message: message.text == "testpls")
async def test(message: Message):
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    r = requests.get(
        "https://i.discogs.com/jh5NU8qQ7fIMan3Yi_cjEdsUczWgp6rD_RBHCn0n3Tk/rs:fit/g:sm/q:90/h:601/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTE2MTc2/NzAwLTE2MTA5MDE3/MDItMTEzMS5wbmc.jpeg", 
        allow_redirects=True,
        headers=headers
    )
    photo = BytesIO(r.content)
    await bot.send_photo(message.from_user.id, photo, caption="god pls work")


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
