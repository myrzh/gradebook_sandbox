import sys
import csv
import sqlite3

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem, QHeaderView
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5 import QtCore, uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('assets/main_window.ui', self)
        self.setWindowTitle('JournalSandbox')
        self.clear_table()
        self.subjects_db_con = sqlite3.connect("assets/subjects.sqlite")

        self.db_update_subjects()

        self.load_table_button.clicked.connect(self.load_table)
        self.save_table_as_button.clicked.connect(self.save_table_as)
        self.clear_table_button.clicked.connect(self.clear_table)
        self.add_subjects_button.clicked.connect(self.add_subjects)
        self.delete_subjects_button.clicked.connect(self.delete_subjects)
        self.add_column_button.clicked.connect(self.add_column)
        self.delete_column_button.clicked.connect(self.delete_column)
        self.main_table.cellClicked.connect(self.update_final_marks)
        self.update_final_marks_button.clicked.connect(self.update_final_marks)

        self.r_delegate = ReadOnlyDelegate(self)
        self.rw_delegate = ReadWriteDelegate(self)
        self.main_table.setItemDelegateForColumn(0, self.r_delegate)
        self.main_table.setItemDelegateForColumn(self.main_table.columnCount() - 1, self.r_delegate)
        # self.main_table.setItemDelegateForColumn(0, rw_delegate)

        self.main_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.main_table.horizontalHeader().setSectionResizeMode(self.main_table.columnCount() - 1, QHeaderView.ResizeToContents)

    def clear_table(self):
        self.show_table('default_table.csv')

    def db_update_subjects(self):
        cur = self.subjects_db_con.cursor()
        result = cur.execute("SELECT * FROM subjects_table").fetchall()
        self.SUBJECTS_LIST = [i[1] for i in result]
        # print(self.SUBJECTS_LIST)

    def verify_cell(self, cell_data: str):
        allowed_symbols = '0123456789.*'

        for symb in cell_data:
            if symb not in allowed_symbols:
                return False
        
        if '*' not in cell_data:
            try:
                int(cell_data)
            except ValueError:
                return False
        elif '*' in cell_data:
            astro_index = cell_data.find('*')
            before_astro = cell_data[:astro_index]
            after_astro = cell_data[astro_index + 1:]
            if after_astro.startswith('.'):
                return False
            try:
                int(before_astro)
                float(after_astro)
            except ValueError:
                return False
        
        return True


    def calculate_final_mark(self, marks_list: list):
        marks_list = [''.join(i.split()) for i in marks_list]
        marks_list = list(filter(None, marks_list))

        if not marks_list:
            return ''
        for cell_data in marks_list:
            if not self.verify_cell(cell_data):
                return 'X*XX'
        
        for index, item in enumerate(marks_list):
            if '*' not in item:
                marks_list[index] = marks_list[index] + '*1'
        
        numerator = eval('+'.join(marks_list))
        coefficients = []

        for exp in marks_list:
            temp_index = exp.find('*')
            coefficients.append(float(exp[temp_index + 1:]))
        denominator = sum(coefficients)

        bad_endings = [f'.{i}' for i in range(0, 10)]
        result = str(round(numerator / denominator, 2))
        if result[-2:] in bad_endings:
            result += '0'
        return result

    def update_final_marks(self):
        rows = self.main_table.rowCount()
        columns = self.main_table.columnCount()
        if rows != 0:
            for row_index in range(0, rows):
                marks_list = []
                for column_index in range(1, columns - 1):
                    # print(row_index, column_index)
                    if self.main_table.item(row_index, column_index) is None:
                        current_cell = ''
                    else:
                        current_cell = self.main_table.item(row_index, column_index).text()
                    marks_list.append(current_cell)
                # print(marks_list)
                final_mark = self.calculate_final_mark(marks_list)
                item = QTableWidgetItem(final_mark)
                self.main_table.setItem(row_index, columns - 1, item)


    def show_table(self, table_name: str):
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
        # print(self.main_table.columnCount())
        # print(self.main_table.horizontalHeaderItem(columnPosition - 2).text())
        self.main_table.setItemDelegateForColumn(self.main_table.columnCount() - 1, self.rw_delegate)
        self.main_table.insertColumn(self.main_table.columnCount() - 1)
        self.main_table.setItemDelegateForColumn(self.main_table.columnCount() - 1, self.r_delegate)
        # self.main_table.horizontalHeaderItem(self.main_table.columnCount() - 2).setText('')
        # TODO: fix numbered headers issue
    
    def delete_column(self):
        pass
        # TODO: similar to add_column method

    def add_subjects(self):
        dlg = AddSubject(self.SUBJECTS_LIST)
        if dlg.exec_():
            used_subjects = []
            if self.main_table.rowCount() > 0:
                for index in range(0, self.main_table.rowCount()):
                    used_subjects.append(self.main_table.item(index, 0).text())
            # print(used_subjects)

            subjects_to_add = dlg.get_checked_subjects()
            # print(subjects_to_add)
            for subject in subjects_to_add:
                if subject not in used_subjects:
                    self.main_table.insertRow(self.main_table.rowCount())
                    item = QTableWidgetItem(subject)   # create a new Item
                    self.main_table.setItem(self.main_table.rowCount() - 1, 0, item)


    def delete_subjects(self):
        dlg = DeleteSubject(self.SUBJECTS_LIST)
        if dlg.exec_():
            subjects_to_delete = dlg.get_checked_subjects()
            # print(subjects_to_delete)
            if self.main_table.rowCount() > 0:
                for index in range(self.main_table.rowCount() - 1, -1, -1):
                    temp_subject = self.main_table.item(index, 0).text()
                    if temp_subject in subjects_to_delete:
                        self.main_table.removeRow(index)
    
    def get_subjects_list(self):
        return self.SUBJECTS_LIST


class AddSubject(QDialog):
    def __init__(self, subjects_list: list):
        super().__init__()
        self.subjects_list = subjects_list
        uic.loadUi('assets/edit_subjects.ui', self)

        for subject in self.subjects_list:
            item = QListWidgetItem()
            item.setText(subject)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.subjects_listwidget.addItem(item)
        
        self.setWindowTitle('Добавить предметы')

    def get_checked_subjects(self):
        checked_items = []
        for index in range(self.subjects_listwidget.count()):
            if self.subjects_listwidget.item(index).checkState() == 2:
                checked_items.append(self.subjects_listwidget.item(index).text())
        return checked_items

class DeleteSubject(AddSubject):
    def __init__(self, subjects_list: list):
        super().__init__(subjects_list)
        self.setWindowTitle('Удалить предметы')


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class ReadWriteDelegate(QStyledItemDelegate):
    pass


def main():
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
