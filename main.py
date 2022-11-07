import sys
import csv
import sqlite3

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QPushButton, QTableWidgetItem, QDialog, QFileDialog, QListWidgetItem
from PyQt5 import QtCore, uic, QtGui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main_window.ui', self)
        self.setWindowTitle('JournalSandbox')
        self.show_table('default_table.csv')
        self.subjects_db_con = sqlite3.connect("subjects.sqlite")

        self.db_update_subjects()

        self.load_table_button.clicked.connect(self.load_table)
        self.save_table_button.clicked.connect(self.save_table)
        self.add_subjects_button.clicked.connect(self.add_subjects_button_clicked)
        self.delete_subjects_button.clicked.connect(self.delete_subjects_button_clicked)

    def db_update_subjects(self):
        cur = self.subjects_db_con.cursor()
        result = cur.execute("SELECT * FROM subjects_table").fetchall()
        self.SUBJECTS_LIST = [i[1] for i in result]
        print(self.SUBJECTS_LIST)


    def show_table(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            title = next(reader)
            self.main_table.setColumnCount(len(title))
            self.main_table.setHorizontalHeaderLabels(title)
            self.main_table.setRowCount(0)
            for i, row in enumerate(reader):
                self.main_table.setRowCount(
                    self.main_table.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.main_table.setItem(
                        i, j, QTableWidgetItem(elem))
        self.main_table.resizeColumnsToContents()

    def load_table(self):
        path = QFileDialog.getOpenFileName(self, 'Загрузить таблицу', '',
                                           'Таблица CSV (*.csv)')[0]
        if path:
            self.show_table(path)
    
    def save_table(self):
        path = QFileDialog.getSaveFileName(self, 'Сохранить таблицу', '',
                                           'Таблица CSV (*.csv)')[0]
        if path:
            with open(str(path), 'wb') as stream:
                writer = csv.writer(stream)
                for row in range(self.main_table.rowCount()):
                    rowdata = []
                    for column in range(self.main_table.columnCount()):
                        item = self.main_table.item(row, column)
                        if item is not None:
                            rowdata.append(
                                str(item.text()).encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)


    def add_subjects_button_clicked(self):
        dlg = AddSubject(self.SUBJECTS_LIST)
        dlg.exec()
    
    def delete_subjects_button_clicked(self):
        dlg = DeleteSubject()
        dlg.exec()
    
    def get_subjects_list(self):
        return self.SUBJECTS_LIST


class AddSubject(QDialog):
    def __init__(self, subjects_list):
        super().__init__()
        self.subjects_list = subjects_list
        self.initUI()

    def initUI(self):
        uic.loadUi('edit_subjects.ui', self)
        self.setWindowTitle('Добавить предметы')
        for subject in self.subjects_list:
            item = QListWidgetItem()
            item.setText(subject)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.subjects_listwidget.addItem(item)
        
    def checked_method(self):
        checked_items = []
        for index in range(self.subjects_listwidget.count()):
            if self.subjects_listwidget.item(index).checkState() == 1:
                checked_items.append(self.subjects_listwidget.item(index).text())
 

class DeleteSubject(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        uic.loadUi('edit_subjects.ui', self)
        self.setWindowTitle('Удалить предметы')


def main():
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
