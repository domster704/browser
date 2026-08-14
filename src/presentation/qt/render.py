import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Browser")
        button = QPushButton("Click me", self)

        self.setCentralWidget(button)


window = MainWindow()
window.show()
