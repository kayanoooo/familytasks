# models.py
from datetime import datetime

class FamilyMember:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
    
    def __str__(self):
        return f"{self.name} (ID: {self.member_id})"
    
    def __repr__(self):
        return f"FamilyMember({self.member_id}, '{self.name}')"

class Task:
    def __init__(self, task_id, title, description, points):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.points = points
        self.assigned_to = None
        self.deadline = None
        self.completed = False
    
    def assign(self, member_id, deadline):
        self.assigned_to = member_id
        self.deadline = deadline
    
    def mark_completed(self):
        self.completed = True
    
    def __str__(self):
        status = "✓" if self.completed else "✗"
        assigned = f", назначена: {self.assigned_to}" if self.assigned_to else ""
        deadline = f", до {self.deadline}" if self.deadline else ""
        return f"{self.task_id}: {self.title} ({self.points} баллов){assigned}{deadline} [{status}]"
    
    def __repr__(self):
        return f"Task({self.task_id}, '{self.title}', '{self.description}', {self.points})"