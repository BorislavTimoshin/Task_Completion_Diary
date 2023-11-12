from PyQt5.QtWidgets import QMessageBox


class WarningDialogWindow:
    @staticmethod
    def len_task_more_15():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Длина названия задачи должна быть не более 20 символов")
        msg.setWindowTitle("Ошибка в названии задачи")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def len_title_result_more_15():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Длина названия результата должна быть не более 10 символов")
        msg.setWindowTitle("Ошибка в названии результата")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def task_exists():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Задание с таким именем уже существует")
        msg.setWindowTitle("Ошибка в названии задачи")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()


warning_dialog_window = WarningDialogWindow()
