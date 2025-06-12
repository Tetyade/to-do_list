from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem, QApplication, QSizePolicy
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from views.task_widget import TaskWidget
from models.task_model import Task
import json
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cyberpunk To-Do")
        self.setFixedSize(400, 600)

        self._load_stylesheet("styles/dark.qss")

        self.tasks = []
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.title_label = QLabel("To-Do")
        self.title_label.setObjectName("title_label")
        self.title_label.setFont(QFont("Audiowide", 24))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(10)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Add a new directive...")
        self.input.setFont(QFont("Audiowide", 10)) 

        self.add_button = QPushButton("ADD")
        self.add_button.setFont(QFont("Audiowide", 10, QFont.Bold))

        self.input_layout.addWidget(self.input)
        self.input_layout.addWidget(self.add_button)
        self.layout.addLayout(self.input_layout)

        self.task_list = QListWidget()
        self.task_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 


        self.layout.addWidget(self.task_list)
        # self.layout.addStretch()

        self.add_button.clicked.connect(self.add_task)

        self.load_tasks()
        self.refresh_task_list()

    def _load_stylesheet(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Error: Stylesheet file '{filename}' not found.")

    def add_task(self):
        title = self.input.text().strip()
        if title:
            task = Task(title)
            self.tasks.append(task)
            self.input.clear()
            self.refresh_task_list()
            self.save_tasks()

    def delete_task(self, task_to_delete):
    # Видаляємо з моделі
        self.tasks = [t for t in self.tasks if t != task_to_delete]
        
        # Оновлюємо UI
        self.refresh_task_list()
        
        # Зберігаємо
        self.save_tasks()

    def refresh_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            widget = TaskWidget(task)
            widget.task_state_changed.connect(self.save_tasks)
            widget.task_deleted.connect(self.delete_task)

            item = QListWidgetItem(self.task_list)
            item.setSizeHint(widget.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, widget)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
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
        print("Saving tasks...")
        with open("tasks.json", "w") as f:
            json.dump([t.__dict__ for t in self.tasks], f, indent=2)