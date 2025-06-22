from database import Database
from models import FamilyMember, Task

class FamilyTaskManager:
    def __init__(self):
        self.db = Database()
        self.load_data()
    
    def load_data(self):
        self.members = self.db.get_members()
        self.tasks = self.db.get_tasks()
    
    def add_member(self, name):
        member_id = self.db.add_member(name)
        member = FamilyMember(member_id, name)
        self.members.append(member)
        return member
    
    def add_task(self, title, description, points):
        task_id = self.db.add_task(title, description, points)
        task = Task(task_id, title, description, points)
        self.tasks.append(task)
        return task
    
    def assign_task(self, task_id, member_id, deadline):
        self.db.assign_task(task_id, member_id, deadline)
        task = self.get_task(task_id)
        if task:
            task.assign(member_id, deadline)

    def remove_member(self, member_id):
        success = self.db.remove_member(member_id)
        if success:
            self.members = [m for m in self.members if m.member_id != member_id]
            for task in self.tasks:
                if task.assigned_to == member_id:
                    task.assigned_to = None
                    task.deadline = None
        return success
    
    def remove_task(self, task_id):
        success = self.db.remove_task(task_id)
        if success:
            self.tasks = [t for t in self.tasks if t.task_id != task_id]
        return success
    
    def complete_task(self, task_id):
        success = self.db.complete_task(task_id)
        if success:
            task = self.get_task(task_id)
            if task:
                task.mark_completed()
        return success
    
    def get_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None
    
    def get_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def get_available_tasks(self):
        return [task for task in self.tasks if not task.assigned_to and not task.completed]
    
    def get_assigned_tasks(self):
        return [task for task in self.tasks if task.assigned_to and not task.completed]
    
    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]
    
    def get_rewards(self):
        return self.db.get_rewards()
    
    def close(self):
        self.db.close()