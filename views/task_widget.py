from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, pyqtSignal # Додаємо pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QColor, QPen

class TaskWidget(QWidget):
    # Новий сигнал, який буде випромінюватися при зміні стану чекбоксу
    task_state_changed = pyqtSignal()

    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self._opacity = 1.0 if task.is_done else 0.0

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(task.is_done)

        self.label = QLabel(task.title)
        self.label.setFont(QFont("Arial", 12))
        self.label.setStyleSheet("color: white; background: transparent;") # Важливо: фон QLabel прозорий

        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.label)
        self.layout.addStretch()

        self.checkbox.stateChanged.connect(self.on_check_changed)

        # Оновлюємо стиль тексту, якщо задача вже виконана
        self._apply_text_color()

    def on_check_changed(self, state):
        self.task.is_done = state == Qt.Checked
        self._apply_text_color()
        self.animate_strike()
        self.task_state_changed.emit() # Випромінюємо сигнал тут!

    def _apply_text_color(self):
        if self.task.is_done:
            self.label.setStyleSheet("color: grey; background: transparent;")
        else:
            self.label.setStyleSheet("color: white; background: transparent;")

    def animate_strike(self):
        print(f"Animate strike: task done = {self.task.is_done}")
        self.anim = QPropertyAnimation(self, b"opacity")
        self.anim.setDuration(400)
        if self.task.is_done:
            self.anim.setStartValue(0.0)
            self.anim.setEndValue(1.0)
        else:
            self.anim.setStartValue(1.0)
            self.anim.setEndValue(0.0)
        self.anim.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._opacity > 0.01:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            neon_color = QColor(255, 0, 255, int(255 * self._opacity))

            pen = QPen(neon_color)
            pen.setWidth(2)
            painter.setPen(pen)

            label_rect = self.label.geometry()
            y = label_rect.y() + label_rect.height() // 2
            x1 = label_rect.x()
            x2 = label_rect.x() + label_rect.width()
            painter.drawLine(x1, y, x2, y)

            glow_strength = 0.5
            glow_color = QColor(255, 0, 255, int(255 * self._opacity * glow_strength))

            for i in range(1, 3):
                glow_pen = QPen(glow_color)
                glow_pen.setWidth(1)
                painter.setPen(glow_pen)
                painter.drawLine(x1, y - i, x2, y - i)
                painter.drawLine(x1, y + i, x2, y + i)

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.update()

    opacity = pyqtProperty(float, get_opacity, set_opacity)