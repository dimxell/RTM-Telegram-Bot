from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def startup_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    markup.add(KeyboardButton("Поиск по релизу"))
    markup.add(KeyboardButton("Поиск по исполнителю"))

    return markup


def gen_titles_inline_keyboard(titles: list[str]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    for title in titles:
        markup.add(InlineKeyboardButton(title, callback_data=title))

    return markup
