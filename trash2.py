from PyQt5 import QtCore, QtWidgets


class Widget_5(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(Widget_5, self).__init__(parent)

        btn = QtWidgets.QPushButton('btn', minimumHeight=50)
        _widget = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(_widget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(btn)

        self.lbl = QtWidgets.QLabel(
            'lbl',
            alignment=QtCore.Qt.AlignCenter,
            styleSheet='font-size: 22px; color: #001E6C;'
        )

        self.frame_1 = QtWidgets.QFrame(
            styleSheet='background-color: #5089C6;'
        )
        vlay = QtWidgets.QVBoxLayout(self.frame_1)
        self.lbl_1 = QtWidgets.QLabel(
            'frame_1',
            self.frame_1,
            alignment=QtCore.Qt.AlignCenter,
            styleSheet='font-size: 22px; color: #FFAA4C;'
        )
        vlay.addWidget(self.lbl_1)

        self.frame_2 = QtWidgets.QFrame(
            styleSheet='background-color: #035397;',
            minimumHeight=150
        )
        vlay = QtWidgets.QVBoxLayout(self.frame_2)
        self.lbl_2 = QtWidgets.QLabel(
            'frame_2',
            self.frame_2,
            alignment=QtCore.Qt.AlignCenter,
            styleSheet='font-size: 22px; color: #FFAA4C;'
        )
        vlay.addWidget(self.lbl_2)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(_widget, 0, 0)
        self.layout.addWidget(self.lbl, 0, 1)
        self.layout.addWidget(self.frame_1, 0, 2)
        self.layout.addWidget(self.frame_2, 1, 2)

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 3)
        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 2)


class Button(QtWidgets.QPushButton):
    pass


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        page1 = QtWidgets.QLabel("page1", alignment=QtCore.Qt.AlignCenter)
        page2 = QtWidgets.QLabel("page2", alignment=QtCore.Qt.AlignCenter)
        page3 = QtWidgets.QLabel("page3", alignment=QtCore.Qt.AlignCenter)
        page4 = QtWidgets.QLabel("page4", alignment=QtCore.Qt.AlignCenter)
        page5 = Widget_5(self)
        page6 = QtWidgets.QLabel("page6", alignment=QtCore.Qt.AlignCenter)

        options = ["Page1", "Page2", "Page3", "Page4", "Page5", "Page6"]
        stackedwidget = QtWidgets.QStackedWidget()

        hlay = QtWidgets.QHBoxLayout()
        group = QtWidgets.QButtonGroup(self)
        group.buttonClicked[int].connect(stackedwidget.setCurrentIndex)

        for i, (option, widget) in enumerate(
                zip(
                    options,
                    (page1, page2, page3, page4, page5, page6)
                )
        ):
            button = Button(text=option, checkable=True)
            ix = stackedwidget.addWidget(widget)
            group.addButton(button, ix)
            hlay.addWidget(button)
            if i == 0:
                button.setChecked(True)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(stackedwidget)
        vbox.addLayout(hlay)


QSS = """
Button {
    background-color: #00ff00;
}
Button:checked {
    background-color: #ff0000;
}
QLabel {
    font-size: 48px;
    color: #B85C38;
}
"""

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setStyleSheet(QSS)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())