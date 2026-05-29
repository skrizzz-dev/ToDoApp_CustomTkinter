import sqlite3

def init_db():
    # Установление соединения с базой данных
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    # Создание таблицу Tasks
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    completed INTEGER DEFAULT 0
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
    WHERE completed = 0
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_completed_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT title, description FROM tasks
    WHERE completed = 1
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows
    
def mark_task_completed(title, description):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE tasks SET completed = 1
    WHERE title = ? AND description = ?
    ''', (title, description))
    conn.commit()
    conn.close()

def return_task_to_active(title, description):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE tasks
    SET completed = 0
    WHERE title = ? AND description = ?
    AND completed = 1
    ''', (title, description))
    conn.commit()
    conn.close()

def clear_all_completed_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM tasks
    WHERE completed = 1
    ''')
    conn.commit()
    conn.close()