from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import TOKEN
from database import get_user, add_user, create_table

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    name = update.effective_user.first_name
    user = get_user(telegram_id)
    if not user:
        add_user(telegram_id, name)
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я Study Mentor.\n"
        "Помогаю готовиться к экзаменам."
    )

async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    user = get_user(telegram_id)
    if user:
        await update.message.reply_text(
            f"👤 Имя: {user[2]}\n"
            f"✅ Выполнено заданий: {user[3]}"
        )
    else:
        await update.message.reply_text(
            "Пользователь не найден"
        )


def main():
    create_table()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("me", me))

    print("Бот запущен...")

    app.run_polling()


if __name__ == "__main__":
    main()