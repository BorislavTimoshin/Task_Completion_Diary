from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QComboBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QAbstractScrollArea, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from main_buttons import CreateTask, AddEntry
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
        self.save_data = QAction(QIcon("Images/table.png"), "Сохранить таблицу", self)
        self.show_chart = QAction(QIcon("Images/chart.png"), "Показать график", self)
        self.program_version = QAction(QIcon("Images/version.jpg"), "Версия программы", self)

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Файл")
        self.data_menu = self.menu.addMenu("Данные")
        self.about_program_menu = self.menu.addMenu("О программе")

        self.file_menu.addAction(self.download_chart)
        self.data_menu.addAction(self.save_data)
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

        self.btn_delete_entry = QPushButton("Удалить запись", self.horizontalLayoutWidget)
        self.btn_delete_entry.setGeometry(460, 40, 141, 31)
        self.horizontalLayout.addWidget(self.btn_delete_entry)

        light_blue_color = "QPushButton""{""background-color : lightblue;""}"
        self.btn_create_task.setStyleSheet(light_blue_color)
        self.btn_new_entry.setStyleSheet(light_blue_color)
        self.btn_delete_entry.setStyleSheet(light_blue_color)

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

        stylesheet = "::section{Background-color:#FFC973}"
        self.table.horizontalHeader().setStyleSheet(stylesheet)

        self.fill_table()

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
        if task is None:
            task = self.btn_open_task.currentText()
        task_names = db.get_task_names(self.id_person)
        index_task = task_names.index(task)
        row = 0
        results = db.get_results(self.id_person)[index_task]
        dates = db.get_dates(self.id_person)[index_task]
        marks = db.get_marks(self.id_person)[index_task]
        comments = db.get_marks(self.id_person)[index_task]
        self.table.setRowCount(len(results))

        for result, date, mark, comment in zip(results, dates, marks, comments):
            self.table.setItem(row, 0, QTableWidgetItem(str(result)))
            self.table.setItem(row, 1, QTableWidgetItem(str(date.date())))
            self.table.setItem(row, 2, QTableWidgetItem(mark))
            self.table.setItem(row, 3, QTableWidgetItem(comment))
            row += 1

    def open_task(self, index):
        task = self.btn_open_task.model().itemFromIndex(index).text()
        task_names = db.get_task_names(self.id_person)
        index_task = task_names.index(task)
        result_name = db.get_result_names(self.id_person)[index_task]
        self.result_value.setText(result_name)
        self.table.setHorizontalHeaderItem(0, self.result_value)
        self.fill_table(task)
