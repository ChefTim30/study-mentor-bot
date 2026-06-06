from config import BOT_NAME, VERSION
from models.user import User
from database import create_table, add_user, get_all_users, create_tasks_table, fill_tasks


# Настройка проекта
print(BOT_NAME)
print(f"Версия: {VERSION}")

# Создаём пользователя через класс
#user = User("Timur")

#user.add_topic("Python")
#user.add_topic("Списки")
#user.add_topic("Функции")

#user.complete_task()
#user.complete_task()

#user.save()

#user.show_info()

print(f"Имя: {user.name}")
print(f"Темы: {user.topics}")
print(f"Выполнено заданий: {user.completed_tasks}")

# Работа с базой данных
create_table()  # Создаём таблицу, если ещё нет
add_user(user.name, user.completed_tasks)  # Добавляем пользователя


# Вывод всех пользователей из базы
all_users = get_all_users()
for u in all_users:
    print(f"ID: {u[0]}, Имя: {u[1]}, Выполнено заданий: {u[2]}")

print("Создаю таблицу tasks...")
create_tasks_table()
from database import  fill_tasks
print("Заполняю задачи...")
fill_tasks()

