from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QDialogButtonBox, QFormLayout, QTableWidgetItem
from PyQt5.QtWidgets import QDialog, QComboBox
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
        self.name_task.setPlaceholderText("Например, экзамен")
        form_layout.addRow(self.title_name_task, self.name_task)

        self.title_name_result = "Название результата (не более 10 символов)"
        self.name_result = QLineEdit(self)
        self.name_result.setPlaceholderText("Например, оценка")
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
                if len(result_name) <= 10:
                    task_names = db.get_task_names(self.id_person)
                    if task_name in task_names:
                        warning_dialog_window.task_exists()
                    else:
                        pass
                        db.set_new_task(self.id_person, task_name, result_name, measurement)
                        self.close()
                        self.parent.btn_open_task.addItem(task_name)
                        self.parent.btn_open_task.setCurrentText(task_name)
                        self.parent.result_value.setText(result_name)
                        self.parent.table.setHorizontalHeaderItem(0, self.parent.result_value)
                        self.parent.result_value.setForeground(QColor(249, 159, 100))
                        if self.parent.btn_open_task.itemText(0) == "Задача не создана":
                            self.parent.btn_open_task.removeItem(0)
                else:
                    warning_dialog_window.len_title_result_more_15()
            else:
                warning_dialog_window.len_task_more_15()
