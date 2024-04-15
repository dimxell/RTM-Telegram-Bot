from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def startup_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    markup.add(KeyboardButton("Поиск по релизу"))
    markup.add(KeyboardButton("Поиск по исполнителю"))

    return markup
