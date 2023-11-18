from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QComboBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QAbstractScrollArea, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from main_buttons import CreateTask, AddEntry, AboutProgram
from warnings_dialog_window import warning_dialog_window
from database import db


# Класс с главным окном для работы с аккаунтом пользователя
class MainWindow(QMainWindow):
    def __init__(self, id_person):
        super().__init__()
        self.id_person = id_person
        self.initUI()

    def initUI(self):
        self.setGeometry(550, 200, 800, 700)
        self.setWindowTitle("Дневник выполнения спортивных задач")

        self.download_chart = QAction(QIcon("Images/chart.png"), "Скачать график", self)
        self.download_data = QAction(QIcon("Images/table.png"), "Скачать таблицу", self)
        self.show_chart = QAction(QIcon("Images/chart.png"), "Показать график", self)
        self.program_version = QAction(QIcon("Images/version.jpg"), "Версия программы", self)
        self.program_version.triggered.connect(self.about_program_dialog)

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Файл")
        self.data_menu = self.menu.addMenu("Данные")
        self.about_program_menu = self.menu.addMenu("О программе")

        self.file_menu.addAction(self.download_chart)
        self.file_menu.addAction(self.download_data)
        self.data_menu.addAction(self.show_chart)
        self.about_program_menu.addAction(self.program_version)

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(10, 10, 771, 80)
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.btn_create_task = QPushButton("Создать задачу", self.horizontalLayoutWidget)
        self.btn_create_task.setGeometry(160, 40, 131, 31)
        self.horizontalLayout.addWidget(self.btn_create_task)
        self.btn_create_task.clicked.connect(self.create_new_task)

        self.btn_new_entry = QPushButton("Добавить запись", self.horizontalLayoutWidget)
        self.btn_new_entry.setGeometry(310, 40, 131, 31)
        self.horizontalLayout.addWidget(self.btn_new_entry)
        self.btn_new_entry.clicked.connect(self.add_entry_to_table)

        light_blue_color = "QPushButton""{""background-color : lightblue;""}"
        self.btn_create_task.setStyleSheet(light_blue_color)
        self.btn_new_entry.setStyleSheet(light_blue_color)

        self.lbl_open_task = QLabel("<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">"
                                    "Открыть задачу:</span></p></body></html>", self)
        self.lbl_open_task.setGeometry(20, 400, 141, 41)

        task_names = db.get_task_names(self.id_person)
        result_names = db.get_result_names(self.id_person)

        self.btn_open_task = QComboBox(self)
        self.btn_open_task.setGeometry(180, 410, 201, 22)
        self.btn_open_task.addItems(task_names)
        self.btn_open_task.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.btn_open_task.view().pressed.connect(self.open_task)
        current_task = self.btn_open_task.currentText()
        if current_task:
            index_current_task = task_names.index(current_task)
            result_value = result_names[index_current_task]
        else:
            result_value = ""

        self.table = QTableWidget(self)
        self.table.setGeometry(10, 75, 771, 301)
        self.table.setColumnCount(4)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 150)

        self.result_value = QTableWidgetItem(result_value)
        self.date_value = QTableWidgetItem("Дата")
        self.mark_value = QTableWidgetItem("Оценка\nрезультата")
        self.comment_value = QTableWidgetItem("Комментарий к результату")

        self.table.setHorizontalHeaderItem(0, self.result_value)
        self.table.setHorizontalHeaderItem(1, self.date_value)
        self.table.setHorizontalHeaderItem(2, self.mark_value)
        self.table.setHorizontalHeaderItem(3, self.comment_value)

        stylesheet1 = "::section{Background-color:#FFC973}"
        self.table.horizontalHeader().setStyleSheet(stylesheet1)
        stylesheet = "::section{Background-color:#E6E6FA}"
        self.table.verticalHeader().setStyleSheet(stylesheet)

        self.fill_table()

        self.title_delete_entry = QLabel("<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">"
                                         "Удалить запись:</span></p></body></html>", self)
        self.title_delete_entry.setGeometry(20, 480, 141, 21)

        self.delete_row_of_entry = QLineEdit(self)
        self.delete_row_of_entry.setPlaceholderText("Введите номер строки, которую хотите удалить")
        self.delete_row_of_entry.setGeometry(20, 520, 321, 22)

        self.btn_delete_entry = QPushButton("Удалить запись", self)
        self.btn_delete_entry.setGeometry(20, 560, 187, 28)
        self.btn_delete_entry.clicked.connect(self.delete_entry)

    def about_program_dialog(self):
        self.about_program = AboutProgram()
        self.about_program.show()

    def create_new_task(self, is_login_account=False, ex_main_window=None, parent=None, username=None, password=None):
        self.new_task = CreateTask(
            self.btn_open_task,
            self.result_value,
            self.table,
            self.id_person,
            is_login_account,
            ex_main_window,
            parent,
            username,
            password
        )
        self.new_task.show()

    def add_entry_to_table(self):
        self.add_entry = AddEntry(
            self.btn_open_task,
            self.table,
            self.id_person
        )
        self.add_entry.show()

    def fill_table(self, task=None):
        """ Метод заполняющий таблицу данными """
        if task is None:
            task = self.btn_open_task.currentText()
        if task:  # Если задание не пустое
            task_names = db.get_task_names(self.id_person)
            index_task = task_names.index(task)
            results = db.get_results(self.id_person)[index_task]
            dates = db.get_dates(self.id_person)[index_task]
            marks = db.get_marks(self.id_person)[index_task]
            comments = db.get_comments(self.id_person)[index_task]
            row = 0
            self.table.setRowCount(len(results))
            for result, date, mark, comment in zip(results, dates, marks, comments):
                self.table.setItem(row, 0, QTableWidgetItem(str(result)))
                self.table.setItem(row, 1, QTableWidgetItem(str(date.date())))
                self.table.setItem(row, 2, QTableWidgetItem(mark))
                self.table.setItem(row, 3, QTableWidgetItem(comment))
                row += 1

    def open_task(self, index):
        """ Метод, открывающий выбранное пользователем задание и заполняющий таблицу """
        task = self.btn_open_task.model().itemFromIndex(index).text()
        task_names = db.get_task_names(self.id_person)
        index_task = task_names.index(task)
        result_name = db.get_result_names(self.id_person)[index_task]
        self.result_value.setText(result_name)
        self.table.setHorizontalHeaderItem(0, self.result_value)
        self.fill_table(task)

    def delete_entry(self):
        number_entry = self.delete_row_of_entry.text()
        try:
            number_entry = int(number_entry) - 1
        except ValueError:
            warning_dialog_window.is_not_number()
            return
        task = self.btn_open_task.currentText()
        task_names = db.get_task_names(self.id_person)
        index_task = task_names.index(task)
        results = db.get_results(self.id_person)
        dates = db.get_dates(self.id_person)
        marks = db.get_marks(self.id_person)
        comments = db.get_comments(self.id_person)
        if (len(results[index_task]) < number_entry + 1) or number_entry < 0:
            warning_dialog_window.row_not_exists()
        else:
            # Удаляем элементы с номером строки, который ввели
            del results[index_task][number_entry]
            del dates[index_task][number_entry]
            del marks[index_task][number_entry]
            del comments[index_task][number_entry]
            # Заполняем таблицу с новыми данными
            row = 0
            self.table.setRowCount(len(results[index_task]))
            for result, date, mark, comment in zip(results[index_task], dates[index_task], marks[index_task], comments[index_task]):
                self.table.setItem(row, 0, QTableWidgetItem(str(result)))
                self.table.setItem(row, 1, QTableWidgetItem(str(date.date())))
                self.table.setItem(row, 2, QTableWidgetItem(mark))
                self.table.setItem(row, 3, QTableWidgetItem(comment))
                row += 1
            # Добавляем в бд новые данные после удаления
            db.set_results(self.id_person, results)
            db.set_dates(self.id_person, dates)
            db.set_marks(self.id_person, marks)
            db.set_comments(self.id_person, comments)
