from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QColor, QPen

class TaskWidget(QWidget):
    task_state_changed = pyqtSignal()
    task_deleted = pyqtSignal(object)

    def __init__(self, task, parent=None):
        super().__init__(parent)

        self.setObjectName("task_widget")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding) 

        self.task = task
        self._opacity = 1.0 if task.is_done else 0.0

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(task.is_done)
        self.checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.checkbox.setMinimumSize(24, 24)

        self.label = QLabel(task.title)
        self.label.setFont(QFont("Audiowide", 12))
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.label.setMinimumWidth(100)

        self.delete_button = QPushButton("X")
        self.delete_button.setFixedSize(20, 20)
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.label)
        self.layout.addStretch(1) 
        self.layout.addWidget(self.delete_button)

        self.checkbox.stateChanged.connect(self.on_check_changed)
        self.delete_button.clicked.connect(self.on_delete_clicked)

        self._apply_text_color()

    def on_check_changed(self, state):
        self.task.is_done = state == Qt.Checked
        self._apply_text_color()
        self.animate_strike()
        self.task_state_changed.emit()

    def on_delete_clicked(self):
        self.task_deleted.emit(self.task)

    def _apply_text_color(self):
        if self.task.is_done:
            self.label.setStyleSheet("color: #777777;")
        else:
            self.label.setStyleSheet("color: white;")

    def animate_strike(self):
        self.anim = QPropertyAnimation(self, b"opacity")
        self.anim.setDuration(400)
        self.anim.setStartValue(0.0 if self.task.is_done else 1.0)
        self.anim.setEndValue(1.0 if self.task.is_done else 0.0)
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
            x1 = label_rect.x()
            x2 = label_rect.x() + label_rect.width()
            y = label_rect.y() + label_rect.height() // 2
            
            painter.drawLine(x1, y, x2, y)

            glow_strength = 0.5
            for i in range(1, 3):
                glow_color = QColor(255, 0, 255, int(255 * self._opacity * (glow_strength / i)))
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

    def sizeHint(self):
        return self.layout.sizeHint()
    