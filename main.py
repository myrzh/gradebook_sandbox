import sys
import csv

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QPushButton, QTableWidgetItem, QDialog, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        uic.loadUi('main_window.ui', self)
        self.show_table('default_table.csv')
        self.add_subjects_button.clicked.connect(self.add_subjects_button_clicked)
        self.delete_subjects_button.clicked.connect(self.delete_subjects_button_clicked)
        self.load_table_button.clicked.connect(self.load_table)

    def show_table(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            title = next(reader)
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()
    
    def load_table(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать таблицу', '',
                                            'Таблица CSV (*.csv);;Все файлы (*)')[0]

    def add_subjects_button_clicked(self):
        dlg = AddSubject()
        dlg.exec()
    
    def delete_subjects_button_clicked(self):
        dlg = DeleteSubject()
        dlg.exec()


class AddSubject(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('edit_subjects.ui', self)
        self.setWindowTitle('Добавить предметы')
        

class DeleteSubject(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('edit_subjects.ui', self)
        self.setWindowTitle('Удалить предметы')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec())