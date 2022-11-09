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
        self.clear_table()
        self.subjects_db_con = sqlite3.connect("subjects.sqlite")

        self.db_update_subjects()

        self.load_table_button.clicked.connect(self.load_table)
        self.save_table_as_button.clicked.connect(self.save_table_as)
        self.clear_table_button.clicked.connect(self.clear_table)
        self.add_subjects_button.clicked.connect(self.add_subjects_button_clicked)
        self.delete_subjects_button.clicked.connect(self.delete_subjects_button_clicked)
        self.add_column_button.clicked.connect(self.add_column)
        self.delete_column_button.clicked.connect(self.delete_column)

    def clear_table(self):
        self.show_table('default_table.csv')

    def db_update_subjects(self):
        cur = self.subjects_db_con.cursor()
        result = cur.execute("SELECT * FROM subjects_table").fetchall()
        self.SUBJECTS_LIST = [i[1] for i in result]
        # print(self.SUBJECTS_LIST)


    def show_table(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
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
        if not path:
            return
        self.show_table(path)
    
    def save_table_as(self):
        path = QFileDialog.getSaveFileName(self, 'Сохранить таблицу как...', '',
                                           'Таблица CSV (*.csv)')[0]
        if not path:
            return
        with open(path, 'w', newline='', encoding="utf8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)   
            writer.writerow(
                [self.main_table.horizontalHeaderItem(i).text()
                for i in range(self.main_table.columnCount())])
            for i in range(self.main_table.rowCount()):
                row = []
                for j in range(self.main_table.columnCount()):
                    item = self.main_table.item(i, j)
                    if item is not None:
                        row.append(item.text())
                writer.writerow(row)

    def add_column(self):
        columnPosition = self.main_table.columnCount()
        self.main_table.insertColumn(columnPosition - 1)
        self.main_table.horizontalHeaderItem(columnPosition - 1).setText('')
        # TODO: fix numbered headers issue
    
    def delete_column(self):
        pass
        # TODO: similar to add_column method

    def add_subjects_button_clicked(self):
        dlg = AddSubject(self.SUBJECTS_LIST)
        if dlg.exec_():
            print(dlg.checked_method())
    
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
            if self.subjects_listwidget.item(index).checkState() == 2:
                checked_items.append(self.subjects_listwidget.item(index).text())
        return checked_items

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
