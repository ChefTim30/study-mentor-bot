from database import add_task

tasks = [
    ("Сколько будет 15 + 27?", "42", 1, "ege", "1"),
    ("Сколько будет 8 × 7?", "56", 1, "ege", "1"),
    ("Найдите значение выражения: 125 - 38", "87", 2, "ege", "1"),
]
for task in tasks:
    add_task(*task)