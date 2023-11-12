import sqlite3
import json


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

    def name_exists(self, username):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `username` FROM `Users` WHERE `username` = ?",
                (username,)
            ).fetchall()
            return bool(result)

    def set_person(self, username, password):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO `Users` (`username`, `password`) VALUES (?, ?)",
                (username, password,)
            )
            self.cursor.execute(
                "INSERT INTO `Tasks` (`id`) VALUES (?)",
                (self.get_id_person(username),)
            )
            self.connection.commit()

    def get_id_person(self, username):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `id` FROM `Users` WHERE `username` = ?",
                (username,)
            ).fetchall()
            for i in result:
                return i[0]

    def get_task_names(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `task_names` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            ).fetchall()
            for i in result:
                return eval(i[0])

    def set_new_task(self, id_person, task_name, result_name, measurement):  # FIXME
        with self.connection:
            task_names = self.get_task_names(id_person)
            if "Задача не создана" in task_names:
                task_names.remove("Задача не создана")
            self.cursor.execute(
                "UPDATE `Tasks` SET `task_names` = ? WHERE `id` = ?",
                (str(task_names + [task_name]), id_person,)
            )
            self.cursor.execute(
                "UPDATE `Tasks` SET `result_names` = ? WHERE `id` = ?",
                (result_name, id_person,)
            )
            self.cursor.execute(
                "UPDATE `Tasks` SET `measurement` = ? WHERE `id` = ?",
                (measurement, id_person,)
            )
            self.connection.commit()


db = Database("database.sqlite")  # Экземпляр класса Database для работы с бд
