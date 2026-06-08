import sqlite3


DB_NAME = "study_mentor.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        name TEXT NOT NULL,
        completed_tasks INTEGER DEFAULT 0,
        grade INTEGER, 
        target_score INTEGER
    )
    """)
    conn.commit()
    conn.close()

def create_tasks_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        difficulty INTEGER DEFAULT 1,
        category TEXT NOT NULL,
        topic TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


def add_user(telegram_id, name, completed_tasks=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (telegram_id, name, completed_tasks) VALUES (?, ?, ?)",
        (telegram_id, name, completed_tasks)
    )
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


ALLOWED_FIELDS = [
    "grade",
    "target_score",
    "completed_tasks"
]

def update_user(telegram_id, field, value):
    conn = get_connection()
    cursor = conn.cursor()
    if field not in ALLOWED_FIELDS:
        raise ValueError(f"Недопустимое поле: {field}")

    cursor.execute(
        f"UPDATE users SET {field} = ? WHERE telegram_id = ?",
        (value, telegram_id)
    )
    conn.commit()
    conn.close()

def add_task(question, answer, difficulty, category, topic):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tasks
        (question, answer, difficulty, category, topic)
        VALUES (?, ?, ?, ?, ?)
        """,
        (question, answer, difficulty, category, topic)
    )
    conn.commit()
    conn.close()


def get_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )
    task = cursor.fetchone()
    conn.close()
    return task

def get_random_task(category, topic, difficulty):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE category = ?
        AND topic = ?
        AND difficulty = ?
        ORDER BY RANDOM()
        LIMIT 1
        """,
        (category, topic, difficulty)
    )
    task = cursor.fetchone()
    conn.close()
    return task



