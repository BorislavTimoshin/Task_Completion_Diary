from PyQt5.QtWidgets import QApplication, QLineEdit, QDialogButtonBox, QFormLayout, QDialog, QComboBox


class NewTask(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Новое задание")
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        form_layout = QFormLayout(self)

        self.title_name_task = "Название задания"
        self.name_task = QLineEdit(self)
        self.name_task.setPlaceholderText("Например, экзамен")
        form_layout.addRow(self.title_name_task, self.name_task)

        self.title_result = "Результат"
        self.result = QLineEdit(self)
        self.result.setPlaceholderText("Например, оценка")
        form_layout.addRow(self.title_result, self.result)

        self.title_unit_of_measurement = "Единица измерения результата"
        self.unit_of_measurement = QComboBox(self)
        self.unit_of_measurement.addItems(["Целое число", "Дробное число", "Время", "Текст"])
        form_layout.addRow(self.title_unit_of_measurement, self.unit_of_measurement)

        form_layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def accept(self):
        return


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = NewTask()
    dialog.exec()
