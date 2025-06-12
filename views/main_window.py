from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem, QApplication # Додаємо QApplication
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from views.task_widget import TaskWidget
from models.task_model import Task
import json
import os

# # Якщо у тебе є цей шрифт, розкоментуй і перевір шлях
# QFontDatabase.addApplicationFont("assets/fonts/Orbitron-Medium.ttf")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cyberpunk To-Do")
        self.setFixedSize(400, 600)

        # Завантажуємо QSS файл
        self._load_stylesheet("styles/dark.qss") # Нова функція для завантаження стилів

        self.tasks = []
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # 1. Заголовок "To-Do"
        self.title_label = QLabel("To-Do")
        self.title_label.setObjectName("title_label") # Встановлюємо objectName для стилізації в QSS
        # Стилі font-size та font-weight ми перенесли в QSS,
        # але QFont для family все ще може бути корисним для fallback або якщо QSS не завантажиться
        self.title_label.setFont(QFont("Orbitron Medium", 24)) # Залишаємо font family, якщо Orbitron завантажено
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # 2. Поле для додавання завдання (об'єднаємо в QHBoxLayout)
        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(10)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Add a new directive...")
        self.input.setFont(QFont("Arial", 10)) # Стиль шрифту залишимо тут, якщо не використовується загальний QWidget font-family

        self.add_button = QPushButton("INITIATE")
        self.add_button.setFont(QFont("Arial", 10, QFont.Bold))

        self.input_layout.addWidget(self.input)
        self.input_layout.addWidget(self.add_button)
        self.layout.addLayout(self.input_layout)

        # 3. Список завдань
        self.task_list = QListWidget()
        # Стилі для QListWidget перенесені в QSS

        self.layout.addWidget(self.task_list)
        self.layout.addStretch()

        self.add_button.clicked.connect(self.add_task)

        self.load_tasks()
        self.refresh_task_list()

    def _load_stylesheet(self, filename):
        """Завантажує QSS файл та застосовує його до додатку."""
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.setStyleSheet(f.read()) # Застосовуємо стилі до головного вікна
                # Або можна застосувати до всього додатку, якщо потрібно:
                # QApplication.instance().setStyleSheet(f.read())
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

    def refresh_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            widget = TaskWidget(task)
            widget.task_state_changed.connect(self.save_tasks)
            
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