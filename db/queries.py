CREATE_TABLE_TASKS = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    quantity TEXT,
    completed INTEGER DEFAULT 0
);
"""

INSERT_TASK = """
INSERT INTO tasks (task, quantity) VALUES (?, ?);
"""

SELECT_TASKS = """
SELECT id, task, quantity, completed FROM tasks;
"""

SELECT_completed = """
SELECT id, task, quantity, completed FROM tasks WHERE completed = 1;
"""

SELECT_uncompleted = """
SELECT id, task, quantity, completed FROM tasks WHERE completed = 0;
"""

UPDATE_TASK = """
UPDATE tasks
SET task = ?, quantity = ?
WHERE id = ?;
"""

UPDATE_TASK_COMPLETED = """
UPDATE tasks
SET completed = ?
WHERE id = ?;
"""

DELETE_TASK = """
DELETE FROM tasks
WHERE id = ?;
"""
