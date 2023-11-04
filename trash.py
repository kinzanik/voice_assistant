import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

class OtherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Другое окно")
        self.setGeometry(100, 100, 400, 200)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.button = QPushButton("Открыть другое окно", self)
        self.button.clicked.connect(self.open_other_window)

    def open_other_window(self):
        other_window = OtherWindow()
        other_window.setParent(self)  # Устанавливаем текущее окно в качестве родителя
        other_window.show()

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())