from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard():
    keyboard = [
        [KeyboardButton("👤 Профиль"), KeyboardButton("📚 Задания")],
        [KeyboardButton("📅 План подготовки"), KeyboardButton("💡 Совет дня")]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )