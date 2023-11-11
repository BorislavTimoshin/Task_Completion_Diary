import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QAbstractScrollArea, QComboBox, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QInputDialog
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt
from authorization import Authorization


if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


# Класс с главным окном для работы с аккаунтом пользователя
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(550, 200, 800, 700)
        self.setWindowTitle("Дневник выполнения задачи")

        self.authorization = Authorization(self)
        self.authorization.show()

        download_chart = QAction(QIcon("Images/chart.png"), "Скачать график", self)
        save_data = QAction(QIcon("Images/table.png"), "Сохранить таблицу", self)
        show_chart = QAction(QIcon("Images/chart.png"), "Показать график", self)
        program_version = QAction(QIcon("Images/version.jpg"), "Версия программы", self)

        menu = self.menuBar()
        file_menu = menu.addMenu("Файл")
        data_menu = menu.addMenu("Данные")
        about_program_menu = menu.addMenu("О программе")

        file_menu.addAction(download_chart)
        data_menu.addAction(save_data)
        data_menu.addAction(show_chart)
        about_program_menu.addAction(program_version)

        self.table = QTableWidget(self)
        self.table.setGeometry(10, 75, 771, 301)
        self.table.setColumnCount(4)
        self.table.setRowCount(1)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.horizontalHeader().setStretchLastSection(True)

        default_task_value = QTableWidgetItem("Результат")
        default_result_value = QTableWidgetItem("Дата")
        default_date_value = QTableWidgetItem("Оценка результата")
        default_comment_value = QTableWidgetItem("Комментарий к результату")

        self.table.setHorizontalHeaderItem(0, default_task_value)
        self.table.setHorizontalHeaderItem(1, default_result_value)
        self.table.setHorizontalHeaderItem(2, default_date_value)
        self.table.setHorizontalHeaderItem(3, default_comment_value)

        default_task_value.setForeground(QColor(249, 159, 100))
        default_result_value.setForeground(QColor(249, 159, 100))
        default_date_value.setForeground(QColor(249, 159, 100))
        default_comment_value.setForeground(QColor(249, 159, 100))

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(10, 10, 771, 80)
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.btn_open_task = QComboBox(self.horizontalLayoutWidget)
        self.btn_open_task.addItem("Открыть задачу")
        self.btn_open_task.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.btn_open_task.setGeometry(10, 40, 131, 31)
        self.horizontalLayout.addWidget(self.btn_open_task)

        self.btn_new_task = QPushButton("Новая задача", self.horizontalLayoutWidget)
        self.btn_new_task.setGeometry(160, 40, 131, 31)
        self.horizontalLayout.addWidget(self.btn_new_task)
        self.btn_new_task.clicked.connect(self.new_task)

        self.btn_new_entry = QPushButton("Добавить запись", self.horizontalLayoutWidget)
        self.btn_new_entry.setGeometry(310, 40, 131, 31)
        self.horizontalLayout.addWidget(self.btn_new_entry)

        self.btn_delete_entry = QPushButton("Удалить запись", self.horizontalLayoutWidget)
        self.btn_delete_entry.setGeometry(460, 40, 141, 31)
        self.horizontalLayout.addWidget(self.btn_delete_entry)

        light_blue_color = "QPushButton""{""background-color : lightblue;""}"
        self.btn_new_task.setStyleSheet(light_blue_color)
        self.btn_new_entry.setStyleSheet(light_blue_color)
        self.btn_delete_entry.setStyleSheet(light_blue_color)

    def new_task(self):
        name_task, ok_pressed = QInputDialog.getText(self, "Новая задача", "Введите название задачи:")
        if ok_pressed:
            print(name_task)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())
