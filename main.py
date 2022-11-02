import sys


from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)  # Загружаем дизайн
        self.initUI()
    
    def initUI(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())