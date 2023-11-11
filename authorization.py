from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from database import db


# Класс для работы с окном: авторизация пользователя
class Authorization(QMainWindow):
    def __init__(self, parent=None):
        super(Authorization, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 700, 400)  # 500
        self.setWindowTitle("Авторизация")

        self.pixmap_authorization = QPixmap("Images/authorization.gif")
        self.image_authorization = QLabel(self)
        self.image_authorization.move(30, 70)
        self.image_authorization.resize(320, 320)
        self.image_authorization.setPixmap(self.pixmap_authorization)

        self.main_title = QLabel('<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">'
                                 'Дневник выполнения задачи</span></p></body></html>', self)
        self.main_title.setGeometry(170, 30, 420, 50)

        self.title_authorization = QLabel('<html><head/><body><p><span style=" font-size:13pt; font-weight:600;">'
                                          'Авторизация аккаунта</span></p></body></html>', self)
        self.title_authorization.setGeometry(330, 110, 261, 61)

        self.text_about_authorization = QLabel('<html><head/><body><p><span style=" font-size:10pt;">Хотите войти или '
                                               'зарегистрироваться?</span></p></body></html>', self)
        self.text_about_authorization.setGeometry(330, 170, 351, 21)

        self.btn_login = QPushButton("Войти", self)
        self.btn_login.setGeometry(330, 200, 131, 28)
        self.btn_login.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )
        self.btn_login.clicked.connect(self.open_login_window)

        self.btn_registration = QPushButton("Регистрация", self)
        self.btn_registration.setGeometry(470, 200, 131, 28)
        self.btn_registration.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )
        self.btn_registration.clicked.connect(self.open_registration_window)

    def open_login_window(self):
        self.close()
        self.login = Login(self.parent)
        self.login.show()

    def open_registration_window(self):
        self.close()
        self.registration = Registration(self.parent)
        self.registration.show()


# Класс для работы с окном: вход пользователя в аккаунт
class Login(QMainWindow):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 700, 500)
        self.setWindowTitle("Вход в аккаунт")

        self.pixmap_authorization = QPixmap("Images/authorization.gif")
        self.image_authorization = QLabel(self)
        self.image_authorization.move(30, 70)
        self.image_authorization.resize(320, 320)
        self.image_authorization.setPixmap(self.pixmap_authorization)

        self.main_title = QLabel('<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">'
                                 'Дневник выполнения задачи</span></p></body></html>', self)
        self.main_title.setGeometry(170, 30, 420, 50)

        self.title_authorization = QLabel('<html><head/><body><p><span style=" font-size:13pt; font-weight:600;">'
                                          'Авторизация аккаунта</span></p></body></html>', self)
        self.title_authorization.setGeometry(330, 110, 261, 61)

        self.info_about_username = QLabel('<html><head/><body><p><span style=" font-size:10pt;">'
                                          'Введите никнейм</span></p></body></html>', self)
        self.info_about_username.setGeometry(330, 170, 191, 20)

        self.username = QLineEdit(self)
        self.username.setGeometry(330, 200, 271, 22)

        self.info_about_password = QLabel('<html><head/><body><p><span style=" font-size:10pt;">'
                                          'Введите пароль</span></p></body></html>', self)
        self.info_about_password.setGeometry(330, 240, 191, 20)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setGeometry(330, 270, 271, 22)

        self.btn_login_account = QPushButton("Войти", self)
        self.btn_login_account.setGeometry(330, 310, 161, 28)
        self.btn_login_account.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )
        self.btn_login_account.clicked.connect(self.login_account)

        self.user_not_exists = QLabel("<html><head/><body><p><span style=\" font-size:10pt; color:#ff3613;\">"
                                      "Пользователя не существует</span></p></body></html>", self)
        self.user_not_exists.setGeometry(300, 360, 261, 51)
        self.user_not_exists.hide()

        self.back_authorization = QPushButton("Вернуться", self)
        self.back_authorization.setGeometry(50, 415, 161, 31)
        self.back_authorization.clicked.connect(self.back_window_authorization)
        self.back_authorization.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )

        self.username.editingFinished.connect(self.login_account)
        self.password.editingFinished.connect(self.login_account)

    def login_account(self):
        username = self.username.text()
        password = self.password.text()
        if username and password:
            if db.person_exists(username, password):
                self.open_main_window()
            else:
                self.user_not_exists.show()

    def back_window_authorization(self):
        self.close()
        self.authorization = Authorization(self.parent)
        self.authorization.show()

    def open_main_window(self):
        self.close()
        self.parent.show()


# Класс для работы с окном: регистрация пользователя
class Registration(QMainWindow):
    def __init__(self, parent=None):
        super(Registration, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 700, 500)
        self.setWindowTitle("Регистрация")

        self.pixmap_authorization = QPixmap("Images/authorization.gif")
        self.image_authorization = QLabel(self)
        self.image_authorization.move(30, 70)
        self.image_authorization.resize(320, 320)
        self.image_authorization.setPixmap(self.pixmap_authorization)

        self.main_title = QLabel('<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">'
                                 'Дневник выполнения задачи</span></p></body></html>', self)
        self.main_title.setGeometry(170, 30, 420, 50)

        self.title_authorization = QLabel('<html><head/><body><p><span style=" font-size:13pt; font-weight:600;">'
                                          'Регистрация аккаунта</span></p></body></html>', self)
        self.title_authorization.setGeometry(330, 110, 261, 61)

        self.info_about_username = QLabel('<html><head/><body><p><span style=" font-size:10pt;">'
                                          'Введите никнейм</span></p></body></html>', self)
        self.info_about_username.setGeometry(330, 170, 191, 20)

        self.username = QLineEdit(self)
        self.username.setGeometry(330, 200, 271, 22)

        self.info_about_password = QLabel('<html><head/><body><p><span style=" font-size:10pt;">'
                                          'Введите пароль</span></p></body></html>', self)
        self.info_about_password.setGeometry(330, 240, 191, 20)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setGeometry(330, 270, 271, 22)

        self.btn_registration_and_login = QPushButton("Зарегистрироваться и войти", self)
        self.btn_registration_and_login.setGeometry(330, 300, 191, 28)
        self.btn_registration_and_login.clicked.connect(self.registration_account)
        self.btn_registration_and_login.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )

        self.back_authorization = QPushButton("Вернуться", self)
        self.back_authorization.setGeometry(50, 415, 161, 31)
        self.back_authorization.clicked.connect(self.back_window_authorization)
        self.back_authorization.setStyleSheet(
            "QPushButton""{"
            "background-color : lightblue;"
            "}"
        )

        self.username.editingFinished.connect(self.registration_account)
        self.password.editingFinished.connect(self.registration_account)

    def registration_account(self):
        username = self.username.text()
        password = self.password.text()
        if username and password:
            db.set_person(username, password)
            self.open_main_window()

    def back_window_authorization(self):
        self.close()
        self.authorization = Authorization(self.parent)
        self.authorization.show()

    def open_main_window(self):
        self.close()
        self.parent.show()

