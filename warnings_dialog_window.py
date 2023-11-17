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
        msg.setText("Длина названия результата должна быть не более 15 символов")
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

    @staticmethod
    def is_not_number():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Введенное значение не является числом")
        msg.setWindowTitle("Ошибка в указании результата")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    @staticmethod
    def len_comment_more_45():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Длина комментария не может быть больше 45 символов")
        msg.setWindowTitle("Ошибка в написании комментария")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()


warning_dialog_window = WarningDialogWindow()
