from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup







def startup_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    markup.add(KeyboardButton("Поиск по релизу"))
    markup.add(KeyboardButton("Поиск по исполнителю"))

    return markup


def gen_titles_inline_keyboard(titles: list[str], countries: list[str], years: list[str], genres: list[str]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    for title, country, year, genre in zip(titles, countries, years, genres):
        markup.add(InlineKeyboardButton(title, callback_data= country + '/' + str(year) + '/' + ''.join(genre)))

    return markup
