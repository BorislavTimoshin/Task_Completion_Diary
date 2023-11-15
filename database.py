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

    def get_result_names(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `result_names` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            ).fetchall()
            for i in result:
                return eval(i[0])

    def get_measurementes(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `measurement` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            ).fetchall()
            for i in result:
                return eval(i[0])

    def set_new_task(self, id_person, task_name, result_name, measurement):
        with self.connection:
            task_names = self.get_task_names(id_person)
            if "Задача не создана" in task_names:
                task_names.remove("Задача не создана")
            self.cursor.execute(
                "UPDATE `Tasks` SET `task_names` = ? WHERE `id` = ?",
                (str(task_names + [task_name]), id_person,)
            )
            result_names = self.get_result_names(id_person)
            self.cursor.execute(
                "UPDATE `Tasks` SET `result_names` = ? WHERE `id` = ?",
                (str(result_names + [result_name]), id_person,)
            )
            measurementes = self.get_measurementes(id_person)
            self.cursor.execute(
                "UPDATE `Tasks` SET `measurement` = ? WHERE `id` = ?",
                (str(measurementes + [measurement]), id_person,)
            )
            self.connection.commit()

    def get_dates(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `dates` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )
            for i in result:
                return eval(i[0])

    def get_results_in_form_date(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `results_in_form_date` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )
            for i in result:
                return eval(i[0])

    def get_results_in_form_int_number(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `results_in_form_int_number` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )
            for i in result:
                return eval(i[0])

    def get_results_in_form_float_number(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `results_in_form_float_number` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )
            for i in result:
                return eval(i[0])

    def get_results_in_form_text(self, id_person):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `results_in_form_text` FROM `Tasks` WHERE `id` = ?",
                (id_person,)
            )
            for i in result:
                return eval(i[0])


db = Database("database.sqlite")  # Экземпляр класса Database для работы с бд
