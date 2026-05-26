import sqlite3

def init_db():
    # Установление соединения с базой данных
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    # Создание таблицу Tasks
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
    title TEXT NOT NULL,
    description TEXT NOT NULL
    );
    ''')
    conn.commit()
    conn.close()
    
def add_task_to_db(title, description):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tasks (title, description) VALUES (?, ?)
    ''', (title, description))
    conn.commit()
    conn.close()

def delete_task_from_db(title, description):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM tasks
    WHERE title = ? AND description = ?
    ''', (title, description))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT title, description FROM tasks
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows
