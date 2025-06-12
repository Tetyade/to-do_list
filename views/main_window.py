from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem
from views.task_widget import TaskWidget
from models.task_model import Task
import json
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cyberpunk To-Do")
        self.setStyleSheet("background-color: #0d0d0d;")

        self.tasks = []
        self.layout = QVBoxLayout(self)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Add a task...")
        self.input.setStyleSheet("background: #1f1f1f; color: #ffffff; padding: 8px;")

        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet("background-color: #ff00ff; color: black; padding: 6px;")

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("background-color: #121212; border: none;")

        self.layout.addWidget(self.input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.task_list)

        self.add_button.clicked.connect(self.add_task)

        self.load_tasks()
        self.refresh_task_list()

    def add_task(self):
        title = self.input.text().strip()
        if title:
            task = Task(title)
            self.tasks.append(task)
            self.input.clear()
            self.refresh_task_list()
            self.save_tasks() # Зберігаємо після додавання

    def refresh_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            widget = TaskWidget(task)
            # Підключаємо сигнал task_state_changed від кожного TaskWidget
            # до методу save_tasks() у MainWindow
            widget.task_state_changed.connect(self.save_tasks)
            
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, widget)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try: # Додаємо try-except для обробки можливих помилок при читанні файлу
                with open("tasks.json", "r") as f:
                    data = json.load(f)
                    self.tasks = [Task(d["title"], d["is_done"]) for d in data]
            except json.JSONDecodeError:
                print("Error loading tasks.json. File might be corrupted.")
                self.tasks = []
            except FileNotFoundError:
                print("tasks.json not found.")
                self.tasks = []


    def save_tasks(self):
        print("Saving tasks...") # Додаємо вивід для відладки
        with open("tasks.json", "w") as f:
            json.dump([t.__dict__ for t in self.tasks], f, indent=2)