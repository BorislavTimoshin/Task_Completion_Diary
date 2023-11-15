import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QTimeEdit, QCalendarWidget
from datetime import datetime
from bisect import bisect_left


class SimplePlanner(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('Минипланировщик')

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget.setFixedSize(300, 300)
        self.verticalLayoutWidget.move(120, 120)

        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.timeEdit = QTimeEdit(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.timeEdit)

        self.calendarWidget = QCalendarWidget(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.calendarWidget)

        self.addEventBtn = QPushButton("Добавить дату", self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.addEventBtn)
        self.addEventBtn.clicked.connect(self.add_event)

        self.dates = []

    def add_event(self):
        date = datetime(
            year=self.calendarWidget.selectedDate().year(),
            month=self.calendarWidget.selectedDate().month(),
            day=self.calendarWidget.selectedDate().day(),
            hour=self.timeEdit.time().hour(),
            minute=self.timeEdit.time().minute()
        )
        ind = bisect_left(self.dates, date)
        self.dates.insert(ind, date)
        print(ind, str(date))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SimplePlanner()
    ex.show()
    sys.exit(app.exec())
