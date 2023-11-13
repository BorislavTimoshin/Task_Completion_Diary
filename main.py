import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QAbstractScrollArea, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt
from authorization import Authorization
from main_buttons import CreateTask
from database import db

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
        self.setWindowTitle("Дневник выполнения спортивных задач")

        authorization = Authorization(self)
        authorization.show()

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

        self.table = QTableWidget(self)
        self.table.setGeometry(10, 75, 771, 301)
        self.table.setColumnCount(4)
        self.table.setRowCount(1)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.result_value = QTableWidgetItem("Результат")
        self.date_value = QTableWidgetItem("Дата")
        self.score_value = QTableWidgetItem("Оценка результата")
        self.comment_value = QTableWidgetItem("Комментарий к результату")

        self.table.setHorizontalHeaderItem(0, self.result_value)
        self.table.setHorizontalHeaderItem(1, self.date_value)
        self.table.setHorizontalHeaderItem(2, self.score_value)
        self.table.setHorizontalHeaderItem(3, self.comment_value)

        self.result_value.setForeground(QColor(249, 159, 100))
        self.date_value.setForeground(QColor(249, 159, 100))
        self.score_value.setForeground(QColor(249, 159, 100))
        self.comment_value.setForeground(QColor(249, 159, 100))

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

        self.btn_delete_entry = QPushButton("Удалить запись", self.horizontalLayoutWidget)
        self.btn_delete_entry.setGeometry(460, 40, 141, 31)
        self.horizontalLayout.addWidget(self.btn_delete_entry)

        light_blue_color = "QPushButton""{""background-color : lightblue;""}"
        self.btn_create_task.setStyleSheet(light_blue_color)
        self.btn_new_entry.setStyleSheet(light_blue_color)
        self.btn_delete_entry.setStyleSheet(light_blue_color)

    def create_new_task(self):
        new_task = CreateTask(self, self.id_person)
        new_task.show()

    def open_task(self, index):
        task = self.btn_open_task.model().itemFromIndex(index).text()
        task_names = db.get_task_names(self.id_person)
        index_task = task_names.index(task)
        result_name = db.get_result_names(self.id_person)[index_task]
        self.result_value.setText(result_name)
        self.table.setHorizontalHeaderItem(0, self.result_value)
        self.result_value.setForeground(QColor(249, 159, 100))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())
