import sys
import os 
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase 
from views.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font_file_name = "Audiowide-Regular.ttf"
    font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", font_file_name)

    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_name = font_families[0]
    window = MainWindow() 
    window.show()
    
    sys.exit(app.exec_())