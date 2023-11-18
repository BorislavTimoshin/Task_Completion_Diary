import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
import sys
import pandas as pd
import os


class CsvCreator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('CSV Creator')
        self.setGeometry(100, 100, 300, 200)

        btn_create_csv = QPushButton('Create CSV', self)
        btn_create_csv.clicked.connect(self.create_csv)
        btn_create_csv.move(100, 80)

    def create_csv(self):
        file_path, file_type = QFileDialog.getSaveFileName(
            self,
            'Скачать таблицу',
            '',
            'All Files(*.xlsx);;CSV Files (*.csv)'
        )
        csv_path = file_path.replace(".xlsx", ".csv")
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Number1', 'Number2'])
            for i in range(1, 11):
                writer.writerow([i, i * 2])
        if file_type == "All Files(*.xlsx)":
            csv_file = pd.read_csv(csv_path)
            excel_file = pd.ExcelWriter(file_path)
            csv_file.to_excel(excel_file, index=False)
            excel_file.save()
            os.remove(csv_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CsvCreator()
    window.show()
    sys.exit(app.exec_())
