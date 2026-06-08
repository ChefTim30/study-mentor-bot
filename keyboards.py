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

def get_categories_keyboard(categories):
    buttons = []
    for category_name in categories:
        buttons.append(
            KeyboardButton(category_name)
        )
    keyboard = []
    for i in range(0, len(buttons), 2):
        keyboard.append(
            buttons[i:i + 2]
        )
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

def get_topics_keyboard(topics):
    buttons = []
    for topic_name in topics:
        buttons.append(
            KeyboardButton(topic_name)
        )
    keyboard = []
    for i in range(0, len(buttons), 4):
        keyboard.append(
            buttons[i:i + 4]
        )
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

def get_difficulties_keyboard():
    keyboard = [
        [
            KeyboardButton("⭐ Легко"),
            KeyboardButton("⭐⭐ Средне"),
            KeyboardButton("⭐⭐⭐ Сложно")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )