import sqlite3


# Класс для работы с базой данных
class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def person_exists(self, username: str, password: str) -> bool:
        with self.connection:
            result = self.cursor.execute(
                "SELECT `username` FROM `Users` WHERE `username` = ? AND `password` = ?",
                (username, password,)
            ).fetchall()
            return bool(result)

    def set_person(self, username, password):
        with self.connection:
            if not self.person_exists(username, password):
                self.cursor.execute(
                    "INSERT INTO `Users` (`username`, `password`) VALUES (?, ?)",
                    (username, password,)
                )
                self.connection.commit()


db = Database("database.sqlite")  # Экземпляр класса Database для работы с бд
