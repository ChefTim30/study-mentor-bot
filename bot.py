from telegram import (
    Update,

)
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import TOKEN
from database import (
    get_user,
    add_user,
    create_table,
    update_user,
    create_tasks_table,
    get_random_task,
    get_task
)
from keyboards import (
    get_main_keyboard,
    get_categories_keyboard,
    get_topics_keyboard,
    get_difficulties_keyboard
)


user_states = {}
current_tasks = {}
selected_categories = {}
selected_topics = {}
CATEGORIES = {
    "📖 ЕГЭ": "ege",
    "💻 Python": "python"
}

TOPICS = {
    "ege": {
        f"📖 №{i}": str(i)
        for i in range(1, 28)
    },
    "python": {
        "🔤 Переменные": "variables",
        "🔀 Условия": "conditions",
        "🔁 Циклы": "loops"
    }
}

DIFFICULTIES = {
    "⭐ Легко": 1,
    "⭐⭐ Средне": 2,
    "⭐⭐⭐ Сложно": 3
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    name = update.effective_user.first_name
    user = get_user(telegram_id)
    if not user:
        add_user(telegram_id, name)
        user_states[telegram_id] = "waiting_for_grade"
        await update.message.reply_text(
            "👋 Привет!\n\n"
            "Я Study Mentor.\n"
            "Помогаю готовиться к экзаменам.\n\n"
            "📚 В каком классе ты учишься?"
        )
    elif user[4] is None:
        user_states[telegram_id] = 'waiting_for_grade'
        await update.message.reply_text(
            "📚 В каком классе ты учишься?"
        )
    elif user[5] is None:
        user_states[telegram_id] = 'waiting_for_target_score'
        await update.message.reply_text(
            "🎯 На сколько баллов ты хочешь сдать экзамен?"
        )
    else:
        await update.message.reply_text(
            "👋 С возвращением!",
            reply_markup=get_main_keyboard()
        )

async def show_profile(update: Update):
    telegram_id = update.effective_user.id
    user = get_user(telegram_id)
    if user:
        await update.message.reply_text(
            f"👤 Имя: {user[2]}\n"
            f"📚 Класс: {user[4]}\n"
            f"🎯 Цель: {user[5]} баллов\n"
            f"✅ Выполнено заданий: {user[3]}"
        )
    else:
        await update.message.reply_text(
            "Пользователь не найден"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    text = update.message.text

    if text == "👤 Профиль":
        await show_profile(update)
        return

    if text == "📚 Задания":
        user_states[telegram_id] = "waiting_for_category"

        await update.message.reply_text(
            "📚 Выберите направление:",
            reply_markup=get_categories_keyboard(CATEGORIES)
        )
        return

    state = user_states.get(telegram_id)

    if state == "waiting_for_grade":
        update_user(telegram_id, "grade", int(text))
        user_states[telegram_id] = "waiting_for_target_score"
        await update.message.reply_text(
            "🎯 На сколько баллов ты хочешь сдать экзамен?"
        )

    elif state == "waiting_for_target_score":
        update_user(telegram_id, "target_score", int(text))
        user_states[telegram_id] = "registered"
        await update.message.reply_text(
            "✅ Вы успешно зарегистрированы!\n"
            "Хорошей подготовки!",
            reply_markup=get_main_keyboard()
        )

    elif state == "waiting_for_category":
        if text not in CATEGORIES:
            await update.message.reply_text(
                "Выберите категорию с помощью кнопок."
            )
            return
        category = CATEGORIES[text]
        selected_categories[telegram_id] = category
        await update.message.reply_text(
            "Выберите тему:",
            reply_markup=get_topics_keyboard(
                TOPICS[category]
            )
        )
        user_states[telegram_id] = "waiting_for_topic"

    elif state == "waiting_for_topic":
        category = selected_categories[telegram_id]
        topics = TOPICS[category]
        if text not in topics:
            await update.message.reply_text(
                "Выберите тему с помощью кнопок."
            )
            return
        topic = topics[text]
        selected_topics[telegram_id] = topic
        await update.message.reply_text(
            "Выберите уровень сложности:",
            reply_markup=get_difficulties_keyboard()
        )
        user_states[telegram_id] = "waiting_for_difficulty"

    elif state == "waiting_for_difficulty":
        if text not in DIFFICULTIES:
            await update.message.reply_text(
                "Выберите сложность с помощью кнопок."
            )
            return
        difficulty = DIFFICULTIES[text]
        category = selected_categories[telegram_id]
        topic = selected_topics[telegram_id]
        task = get_random_task(
            category,
            topic,
            difficulty
        )
        if task is None:
            await update.message.reply_text(
                "Для этой темы пока нет задач."
            )
            return
        current_tasks[telegram_id] = task
        await update.message.reply_text(
            f"📚 Задача\n\n{task[1]}"
        )
        user_states[telegram_id] = "waiting_for_task_answer"

    elif state == "waiting_for_task_answer":
        task = current_tasks[telegram_id]
        user = get_user(telegram_id)
        correct_answer = task[2]
        if text == correct_answer:
            update_user(
                telegram_id,
                "completed_tasks",
                user[3] + 1
            )
            await update.message.reply_text(
                "✅ Верно!",
                reply_markup=get_main_keyboard()
            )
        else:
            await update.message.reply_text(
                f"❌ Неверно. Правильный ответ: {correct_answer}",
                reply_markup = get_main_keyboard()
            )
        user_states.pop(telegram_id, None)
        current_tasks.pop(telegram_id, None)




def main():
    create_table()
    create_tasks_table()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Бот запущен...")

    app.run_polling()


if __name__ == "__main__":
    main()