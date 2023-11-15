from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QDialogButtonBox, QFormLayout, QTextEdit
from PyQt5.QtWidgets import QDialog, QComboBox, QLabel
from PyQt5.QtWidgets import QPushButton, QWidget, QCalendarWidget
from PyQt5.QtWidgets import QVBoxLayout, QTimeEdit
from datetime import datetime
from bisect import bisect_left
from warnings_dialog_window import warning_dialog_window
from database import db


class CreateTask(QDialog):
    def __init__(self, parent=None, id_person=None):
        super().__init__(parent)
        self.parent = parent
        self.id_person = id_person
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Новая задача")

        buttons_new_task = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        form_layout = QFormLayout(self)

        self.title_name_task = "Название задачи (не более 20 символов)"
        self.name_task = QLineEdit(self)
        self.name_task.setPlaceholderText("Например, бег по утрам")
        form_layout.addRow(self.title_name_task, self.name_task)

        self.title_name_result = "Название результата (не более 15 символов)"
        self.name_result = QLineEdit(self)
        self.name_result.setPlaceholderText("Например, дальность (км)")
        form_layout.addRow(self.title_name_result, self.name_result)

        self.title_unit_of_measurement = "Единица измерения результата"
        self.unit_of_measurement = QComboBox(self)
        self.unit_of_measurement.addItems(["Целое число", "Дробное число", "Время", "Текст"])
        form_layout.addRow(self.title_unit_of_measurement, self.unit_of_measurement)

        form_layout.addWidget(buttons_new_task)
        buttons_new_task.accepted.connect(self.accept)
        buttons_new_task.rejected.connect(self.reject)

    def accept(self):
        task_name = self.name_task.text()
        result_name = self.name_result.text()
        measurement = self.unit_of_measurement.currentText()
        if task_name and result_name:
            if len(task_name) <= 20:
                if len(result_name) <= 15:
                    task_names = db.get_task_names(self.id_person)
                    result_names = db.get_result_names(self.id_person)
                    if task_name in task_names:
                        warning_dialog_window.task_exists()
                    else:
                        # FIXME
                        if self.parent.btn_open_task.itemText(0) == "Задача не создана":
                            task_names.remove("Задача не создана")
                            self.parent.btn_open_task.removeItem(0)
                        if result_names[0] == "Результат":
                            del result_names[0]
                        db.set_new_task(self.id_person, task_name, result_name, measurement)
                        self.close()
                        self.parent.btn_open_task.addItem(task_name)
                        self.parent.btn_open_task.setCurrentText(task_name)
                        self.parent.result_value.setText(result_name)
                        self.parent.table.setHorizontalHeaderItem(0, self.parent.result_value)
                        self.parent.result_value.setForeground(QColor(249, 159, 100))
                else:
                    warning_dialog_window.len_title_result_more_15()
            else:
                warning_dialog_window.len_task_more_15()


class AddEntry(QDialog):
    def __init__(self, parent=None, id_person=None):
        super().__init__(parent)
        self.parent = parent
        self.id_person = id_person
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Добавить запись")
        self.setGeometry(550, 200, 800, 700)

        buttons_add_entry = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        self.title_result = QLabel(f"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
                                   f"Укажите {self.get_result_name()}:</span></p></body></html>", self)
        self.title_result.setGeometry(10, 0, 331, 31)

        self.result = QLineEdit(self)
        self.result.setGeometry(10, 40, 261, 31)

        self.title_score = QLabel("<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
                                  "Укажите оценку результата</span></p></body></html>", self)
        self.title_score.setGeometry(10, 90, 271, 31)

        self.score = QComboBox(self)
        self.score.addItems(["1", "2", "3", "4", "5"])
        self.score.setGeometry(10, 130, 261, 31)

        self.title_comment = QLabel("<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
                                    "Напишите комментарий к результату (По желанию). "
                                    "До 45 символов</span></p></body></html>", self)
        self.title_comment.setGeometry(10, 180, 641, 31)

        self.comment = QLineEdit(self)
        self.comment.setGeometry(10, 220, 451, 40)

        self.title_data = QLabel("<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">"
                                 "Укажите дату выполнения спортивной задачи:</span></p></body></html>", self)
        self.title_data.setGeometry(10, 295, 420, 30)

        form_layout = QFormLayout(self)

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget.setGeometry(15, 335, 300, 300)

        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.timeEdit = QTimeEdit(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.timeEdit)

        self.calendarWidget = QCalendarWidget(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.calendarWidget)

        form_layout.addWidget(buttons_add_entry)
        buttons_add_entry.accepted.connect(self.accept)
        buttons_add_entry.rejected.connect(self.reject)

    def get_date(self):
        date = datetime(
            year=self.calendarWidget.selectedDate().year(),
            month=self.calendarWidget.selectedDate().month(),
            day=self.calendarWidget.selectedDate().day(),
            hour=self.timeEdit.time().hour(),
            minute=self.timeEdit.time().minute()
        )
        return date

    def get_result_name(self):
        result_names = db.get_result_names(self.id_person)
        index_result = self.get_index_task()
        result_name = result_names[index_result]
        return result_name

    def get_index_task(self):
        task = self.parent.btn_open_task.currentText()
        tasks = db.get_task_names(self.id_person)
        return tasks.index(task)

    def get_index_insert(self):
        dates = db.get_dates(self.id_person)
        index_insert = bisect_left(dates, self.get_date())
        return index_insert

    def insert_in_db(self):
        date = self.get_date()
        result = None
        index_task = self.get_index_task()
        measurement = db.get_measurementes(self.id_person)
        if measurement == "Целое число":
            pass
        elif measurement == "Дробное число":
            pass
        elif measurement == "Время":
            results_in_form_date = db.get_results_in_form_date(self.id_person)
            if index_task == len(results_in_form_date):
                results_in_form_date.append([])

    def accept(self):
        pass
