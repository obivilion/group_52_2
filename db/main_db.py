import sqlite3
from db import queries
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASKS)
    conn.commit()
    conn.close()

def get_tasks(filter_type="all"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if filter_type == "completed":
        cursor.execute(queries.SELECT_completed)
    elif filter_type == "uncompleted":
        cursor.execute(queries.SELECT_uncompleted)
    else:
        cursor.execute(queries.SELECT_TASKS)

    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task_db(task, quantity="1"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task, quantity))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def update_task_db(task_id, new_task=None, new_quantity=None, completed=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if new_task is not None and new_quantity is not None:
        cursor.execute(queries.UPDATE_TASK, (new_task, new_quantity, task_id))
    if completed is not None:
        cursor.execute(queries.UPDATE_TASK_COMPLETED, (completed, task_id))

    conn.commit()
    conn.close()

def delete_task_db(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()
