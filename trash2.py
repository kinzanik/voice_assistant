import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from math import sqrt


class Calculator(QMainWindow):
    def __init__(self):
        self.temp_num = ''
        self.buff = 0
        self.op = ''
        self.first_op = True
        super().__init__()
        uic.loadUi('untitled.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    ex.show()
    sys.exit(app.exec_())