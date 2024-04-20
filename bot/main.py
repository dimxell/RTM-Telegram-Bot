from configparser import ConfigParser

from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.types import Message, InputMediaPhoto

from bot.keyboards import startup_keyboard, gen_titles_inline_keyboard
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
    stringList = {"Titles": [i.title for i in releases], "Countries": [i.country for i in releases], "Years": [i.release_year for i in releases], "Genres": [i.genres for i in releases]}
    await bot.send_media_group(message.chat.id, [InputMediaPhoto(i.cover_image_url, caption=i.title) for i in releases])
    await bot.send_message(message.from_user.id, "Выбери релиз из списка", reply_markup=gen_titles_inline_keyboard(stringList.get("Titles", 0), stringList.get("Countries", 0), stringList.get("Years", 0), stringList.get("Genres", 0)))
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
async def button_callback(call):
    country = call.data.split('/')[0]
    year = call.data.split('/')[1]
    genre = call.data.split('/')[2]
    await bot.send_message(call.message.chat.id, f'Страна: {country}\n' f'Год выпуска: {year}\n' f'Жанр: {genre}\n')


@bot.message_handler(func=lambda message: message.text == "testpls")
async def test(message: Message):
    await bot.send_photo(message.from_user.id, 
                         'https://i.discogs.com/jh5NU8qQ7fIMan3Yi_cjEdsUczWgp6rD_RBHCn0n3Tk/rs:fit/g:sm/q:90/h:601/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTE2MTc2/NzAwLTE2MTA5MDE3/MDItMTEzMS5wbmc.jpeg', 
                         caption="god pls work")


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
