# database.py
import sqlite3
from datetime import datetime
from models import FamilyMember, Task

class Database:
    def __init__(self, db_name='family_task_manager.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Таблица членов семьи
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        ''')
        
        # Таблица задач
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            points INTEGER NOT NULL,
            assigned_to INTEGER,
            deadline TEXT,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY (assigned_to) REFERENCES members(member_id)
        )
        ''')
        
        # Таблица рейтинга (баллов)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS rewards (
            member_id INTEGER PRIMARY KEY,
            points INTEGER DEFAULT 0,
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        )
        ''')
        
        self.conn.commit()
    
    # Методы для работы с членами семьи
    def add_member(self, name):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO members (name) VALUES (?)', (name,))
        member_id = cursor.lastrowid
        cursor.execute('INSERT INTO rewards (member_id, points) VALUES (?, 0)', (member_id,))
        self.conn.commit()
        return member_id
    
    def get_members(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT member_id, name FROM members')
        return [FamilyMember(row[0], row[1]) for row in cursor.fetchall()]
    
    # Методы для работы с задачами
    def add_task(self, title, description, points):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO tasks (title, description, points) 
        VALUES (?, ?, ?)
        ''', (title, description, points))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_tasks(self, filter_type='all'):
        cursor = self.conn.cursor()
        
        if filter_type == 'available':
            query = 'SELECT * FROM tasks WHERE assigned_to IS NULL AND completed = 0'
        elif filter_type == 'assigned':
            query = 'SELECT * FROM tasks WHERE assigned_to IS NOT NULL AND completed = 0'
        elif filter_type == 'completed':
            query = 'SELECT * FROM tasks WHERE completed = 1'
        else:
            query = 'SELECT * FROM tasks'
        
        cursor.execute(query)
        tasks = []
        for row in cursor.fetchall():
            task = Task(row[0], row[1], row[2], row[3])
            if row[4]:  # assigned_to
                task.assigned_to = row[4]
            if row[5]:  # deadline
                task.deadline = row[5]
            task.completed = bool(row[6])
            tasks.append(task)
        return tasks
    
    def assign_task(self, task_id, member_id, deadline):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE tasks 
        SET assigned_to = ?, deadline = ?
        WHERE task_id = ?
        ''', (member_id, deadline, task_id))
        self.conn.commit()
    
    def complete_task(self, task_id):
        cursor = self.conn.cursor()
        
        # Получаем информацию о задаче
        cursor.execute('SELECT assigned_to, points FROM tasks WHERE task_id = ?', (task_id,))
        task_data = cursor.fetchone()
        
        if not task_data or not task_data[0]:  # Если задачи нет или она не назначена
            return False
        
        member_id, points = task_data
        
        # Помечаем задачу как выполненную
        cursor.execute('UPDATE tasks SET completed = 1 WHERE task_id = ?', (task_id,))
        
        # Обновляем баллы
        cursor.execute('''
        UPDATE rewards 
        SET points = points + ? 
        WHERE member_id = ?
        ''', (points, member_id))
        
        self.conn.commit()
        return True
    
    def get_rewards(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT m.member_id, m.name, r.points 
        FROM members m
        JOIN rewards r ON m.member_id = r.member_id
        ORDER BY r.points DESC
        ''')
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()