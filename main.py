from config import BOT_NAME, VERSION
from models.user import User

print(BOT_NAME)
print(f"Версия: {VERSION}")

user = User("Timur")

user.add_topic("Python")
user.add_topic("Списки")
user.add_topic("Функции")

user.complete_task()
user.complete_task()

print(f"Имя: {user.name}")
print(f"Темы: {user.topics}")
print(f"Выполнено заданий: {user.completed_tasks}")