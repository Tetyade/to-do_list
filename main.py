import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow

app = QApplication(sys.argv)

with open("styles/dark.qss", "r") as f:
    app.setStyleSheet(f.read())


window = MainWindow()
window.show()

sys.exit(app.exec_())
