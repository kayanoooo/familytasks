import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                             QDateEdit, QMessageBox, QTabWidget, QFormLayout, QFrame)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from manager import FamilyTaskManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = FamilyTaskManager()
        self.setWindowTitle("Family Task Manager")
        self.setGeometry(100, 100, 900, 700)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                padding: 5px;
                background: white;
            }
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #d3d3d3;
                padding: 8px 15px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLineEdit, QDateEdit {
                border: 1px solid #d3d3d3;
                border-radius: 4px;
                padding: 6px;
            }
            QListWidget {
                border: 1px solid #d3d3d3;
                border-radius: 4px;
                background: white;
                alternate-background-color: #f9f9f9;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
            .section {
                background: white;
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #e0e0e0;
            }
            QPushButton[background-color="#f44336"] {
            background-color: #f44336;
            }
            QPushButton[background-color="#f44336"]:hover {
                background-color: #d32f2f;
            }
            QPushButton[background-color="#f44336"]:pressed {
                background-color: #b71c1c;
            }
        """)
        
        self.setup_ui()
        self.load_sample_data()
    
    def load_sample_data(self):
        if not self.manager.members:
            self.manager.add_member("Мама")
            self.manager.add_member("Папа")
            self.manager.add_member("Ребенок")
            
            self.manager.add_task("Помыть посуду", "Помыть всю посуду после ужина", 10)
            self.manager.add_task("Купить продукты", "Молоко, хлеб, яйца", 15)
            self.manager.add_task("Заплатить за интернет", "Оплатить счет до 10 числа", 20)
        
        self.update_all_lists()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        central_widget.setLayout(main_layout)
        
        tabs = QTabWidget()
        tabs.setFont(QFont("Arial", 10))
        main_layout.addWidget(tabs)
        
        members_tab = QWidget()
        tabs.addTab(members_tab, "👪 Члены семьи")
        self.setup_members_tab(members_tab)
        
        tasks_tab = QWidget()
        tabs.addTab(tasks_tab, "📋 Задачи")
        self.setup_tasks_tab(tasks_tab)
        
        assign_tab = QWidget()
        tabs.addTab(assign_tab, "📌 Назначение")
        self.setup_assign_tab(assign_tab)
        
        rating_tab = QWidget()
        tabs.addTab(rating_tab, "🏆 Рейтинг")
        self.setup_rating_tab(rating_tab)
    
    def create_section(self, title):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(".QFrame { background: white; border-radius: 5px; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        label = QLabel(title)
        label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        layout.addWidget(label)
        
        return frame, layout
    
    def setup_members_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        add_frame, add_layout = self.create_section("Добавить члена семьи")
        
        form = QFormLayout()
        form.setVerticalSpacing(10)
        
        self.member_name_input = QLineEdit()
        self.member_name_input.setPlaceholderText("Введите имя")
        form.addRow("Имя члена семьи:", self.member_name_input)
        
        add_button = QPushButton("➕ Добавить")
        add_button.clicked.connect(self.add_member)
        form.addRow(add_button)
        
        add_layout.addLayout(form)
        layout.addWidget(add_frame)
        
        list_frame, list_layout = self.create_section("Список членов семьи")
        self.members_list = QListWidget()
        self.members_list.setStyleSheet("QListWidget { font-size: 13px; }")
        list_layout.addWidget(self.members_list)
        layout.addWidget(list_frame)

        delete_member_button = QPushButton("🗑️ Удалить выбранного")
        delete_member_button.clicked.connect(self.remove_member)
        delete_member_button.setStyleSheet("background-color: #f44336;")  # Красный цвет
        form.addRow(delete_member_button)
    
    def setup_tasks_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        add_frame, add_layout = self.create_section("Добавить задачу")
        
        form = QFormLayout()
        form.setVerticalSpacing(10)
        
        self.task_title_input = QLineEdit()
        self.task_title_input.setPlaceholderText("Название задачи")
        form.addRow("Название:", self.task_title_input)
        
        self.task_desc_input = QLineEdit()
        self.task_desc_input.setPlaceholderText("Описание задачи")
        form.addRow("Описание:", self.task_desc_input)
        
        self.task_points_input = QLineEdit()
        self.task_points_input.setPlaceholderText("Баллы за выполнение")
        form.addRow("Баллы:", self.task_points_input)
        
        add_button = QPushButton("➕ Добавить")
        add_button.clicked.connect(self.add_task)
        form.addRow(add_button)
        
        add_layout.addLayout(form)
        layout.addWidget(add_frame)
        
        list_frame, list_layout = self.create_section("Список задач")
        self.tasks_list = QListWidget()
        self.tasks_list.setStyleSheet("QListWidget { font-size: 13px; }")
        list_layout.addWidget(self.tasks_list)
        layout.addWidget(list_frame)

        delete_task_button = QPushButton("🗑️ Удалить выбранную")
        delete_task_button.clicked.connect(self.remove_task)
        delete_task_button.setStyleSheet("background-color: #f44336;")  # Красный цвет
        form.addRow(delete_task_button)
    
    def setup_assign_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        top_frame = QFrame()
        top_frame.setStyleSheet(".QFrame { background: white; border-radius: 5px; }")
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(10, 10, 10, 10)
        
        member_frame, member_layout = self.create_section("Выберите члена семьи")
        self.assign_member_combo = QListWidget()
        self.assign_member_combo.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        member_layout.addWidget(self.assign_member_combo)
        top_layout.addWidget(member_frame)
        
        task_frame, task_layout = self.create_section("Выберите задачу")
        self.assign_task_combo = QListWidget()
        self.assign_task_combo.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        task_layout.addWidget(self.assign_task_combo)
        top_layout.addWidget(task_frame)
        
        layout.addWidget(top_frame)
        
        form_frame, form_layout = self.create_section("Назначение задачи")
        form = QFormLayout()
        form.setVerticalSpacing(10)
        
        self.deadline_input = QDateEdit()
        self.deadline_input.setDate(QDate.currentDate())
        self.deadline_input.setCalendarPopup(True)
        form.addRow("Дедлайн:", self.deadline_input)
        
        assign_button = QPushButton("📌 Назначить задачу")
        assign_button.clicked.connect(self.assign_task)
        form.addRow(assign_button)
        
        form_layout.addLayout(form)
        layout.addWidget(form_frame)
        
        assigned_frame, assigned_layout = self.create_section("Назначенные задачи")
        self.assigned_tasks_list = QListWidget()
        assigned_layout.addWidget(self.assigned_tasks_list)
        
        complete_button = QPushButton("✅ Отметить как выполненную")
        complete_button.clicked.connect(self.complete_task)
        assigned_layout.addWidget(complete_button)
        
        layout.addWidget(assigned_frame)
    
    def setup_rating_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        rating_frame, rating_layout = self.create_section("Рейтинг членов семьи")
        
        self.rating_list = QListWidget()
        self.rating_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:first {
                color: #FFD700;
                font-weight: bold;
            }
            QListWidget::item:nth-child(2) {
                color: #C0C0C0;
                font-weight: bold;
            }
            QListWidget::item:nth-child(3) {
                color: #CD7F32;
                font-weight: bold;
            }
        """)
        
        rating_layout.addWidget(self.rating_list)
        
        refresh_button = QPushButton("🔄 Обновить рейтинг")
        refresh_button.clicked.connect(self.update_rating)
        rating_layout.addWidget(refresh_button)
        
        layout.addWidget(rating_frame)
    
    def add_member(self):
        name = self.member_name_input.text().strip()
        if name:
            self.manager.add_member(name)
            self.member_name_input.clear()
            self.update_members_list()
            QMessageBox.information(self, "Успех", f"Член семьи {name} добавлен!")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите имя члена семьи!")
    
    def add_task(self):
        title = self.task_title_input.text().strip()
        description = self.task_desc_input.text().strip()
        points = self.task_points_input.text().strip()
        
        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название задачи!")
            return
        
        try:
            points = int(points) if points else 0
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Баллы должны быть числом!")
            return
        
        self.manager.add_task(title, description, points)
        self.task_title_input.clear()
        self.task_desc_input.clear()
        self.task_points_input.clear()
        
        self.update_tasks_list()
        self.update_assign_lists()
        
        QMessageBox.information(self, "Успех", f"Задача '{title}' добавлена!")
    
    def remove_member(self):
        selected = self.members_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите члена семьи для удаления!")
            return
        
        member_id = selected.data(Qt.ItemDataRole.UserRole)
        member = self.manager.get_member(member_id)
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            f'Удалить {member.name}? Назначенные задачи останутся без исполнителя!',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.manager.remove_member(member_id):
                self.update_members_list()
                self.update_assign_lists()
                self.update_assigned_tasks_list()
                QMessageBox.information(self, "Успех", "Член семьи удален!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить члена семьи!")
    
    def assign_task(self):
        selected_members = self.assign_member_combo.selectedItems()
        selected_tasks = self.assign_task_combo.selectedItems()
        
        if not selected_members or not selected_tasks:
            QMessageBox.warning(self, "Ошибка", "Выберите и члена семьи, и задачу!")
            return
        
        member_item = selected_members[0]
        task_item = selected_tasks[0]
        
        member_id = member_item.data(Qt.ItemDataRole.UserRole)
        task_id = task_item.data(Qt.ItemDataRole.UserRole)
        
        deadline = self.deadline_input.date().toString("yyyy-MM-dd")
        
        self.manager.assign_task(task_id, member_id, deadline)
        self.update_assigned_tasks_list()
        self.update_tasks_list()
        self.update_assign_lists()
        
        member = self.manager.get_member(member_id)
        task = self.manager.get_task(task_id)
        
        QMessageBox.information(self, "Успех", 
                              f"Задача '{task.title}' назначена на {member.name} до {deadline}!")
    
    def complete_task(self):
        selected_tasks = self.assigned_tasks_list.selectedItems()
        if not selected_tasks:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для отметки!")
            return
        
        task_item = selected_tasks[0]
        task_id = task_item.data(Qt.ItemDataRole.UserRole)
        
        if self.manager.complete_task(task_id):
            self.assigned_tasks_list.takeItem(self.assigned_tasks_list.row(task_item))
            self.update_tasks_list()
            self.update_rating()
            
            task = self.manager.get_task(task_id)
            member = self.manager.get_member(task.assigned_to)
            
            QMessageBox.information(self, "Успех", 
                                  f"Задача '{task.title}' отмечена как выполненная!\n"
                                  f"{member.name} получает {task.points} баллов!")
        else:
            QMessageBox.warning(self, "Ошибка", "Эта задача уже выполнена!")


    def remove_task(self):
        selected = self.tasks_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления!")
            return
        
        task_id = selected.data(Qt.ItemDataRole.UserRole)
        task = self.manager.get_task(task_id)
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            f'Удалить задачу "{task.title}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.manager.remove_task(task_id):
                self.update_tasks_list()
                self.update_assign_lists()
                self.update_assigned_tasks_list()
                QMessageBox.information(self, "Успех", "Задача удалена!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить задачу!")
    
    def update_all_lists(self):
        self.update_members_list()
        self.update_tasks_list()
        self.update_assign_lists()
        self.update_assigned_tasks_list()
        self.update_rating()
    
    def update_members_list(self):
        self.members_list.clear()
        for member in self.manager.members:
            item = QListWidgetItem(f"👤 {member.name} (ID: {member.member_id})")
            item.setData(Qt.ItemDataRole.UserRole, member.member_id)
            self.members_list.addItem(item)
    
    def update_tasks_list(self):
        self.tasks_list.clear()
        for task in self.manager.tasks:
            if not task.completed:
                status = "🔴" if task.assigned_to else "🟢"
                item_text = f"{status} {task.title} ({task.points} баллов)"
                if task.assigned_to:
                    member = self.manager.get_member(task.assigned_to)
                    item_text += f" → {member.name}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, task.task_id)
                self.tasks_list.addItem(item)
    
    def update_assign_lists(self):
        self.assign_member_combo.clear()
        for member in self.manager.members:
            item = QListWidgetItem(f"👤 {member.name}")
            item.setData(Qt.ItemDataRole.UserRole, member.member_id)
            self.assign_member_combo.addItem(item)
        
        self.assign_task_combo.clear()
        for task in self.manager.get_available_tasks():
            item = QListWidgetItem(f"{task.title} ({task.points} баллов)")
            item.setData(Qt.ItemDataRole.UserRole, task.task_id)
            self.assign_task_combo.addItem(item)
    
    def update_assigned_tasks_list(self):
        self.assigned_tasks_list.clear()
        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        
        for task in self.manager.get_assigned_tasks():
            member = self.manager.get_member(task.assigned_to)
            item_text = f"📌 {task.title} (на {member.name}, до {task.deadline}) - {task.points} баллов"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, task.task_id)
            
            if task.deadline < current_date:
                item.setForeground(QColor("red"))
            
            self.assigned_tasks_list.addItem(item)
    
    def update_rating(self):
        self.rating_list.clear()
        rewards = self.manager.get_rewards()
        
        medals = ["🥇", "🥈", "🥉"]
        for i, (member_id, name, points) in enumerate(rewards, 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            item = QListWidgetItem(f"{medal} {name}: {points} баллов")
            self.rating_list.addItem(item)
    
    def closeEvent(self, event):
        self.manager.close()
        event.accept()