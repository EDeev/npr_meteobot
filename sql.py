import sqlite3


class SQLighter:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def user_exists(self, id_user):
        """Проверяем, есть ли уже пользователь в базе"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `id_user` = ?", (id_user,)).fetchall()
            return bool(len(result))

    def add_user(self, id_user):
        """Добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`id_user`, `status`, `send`, `part`, `city`) "
                                       "VALUES(?,?,?,?,?)", (id_user, 0, 1, 0, 0))

    def update_user(self, id_user, win, num):
        """Обновляем статус пользователя"""
        with self.connection:
            if win == 1:
                return self.cursor.execute("UPDATE `users` SET `status` = ? WHERE `id_user` = ?", (num, id_user))
            elif win == 2:
                return self.cursor.execute("UPDATE `users` SET `send` = ? WHERE `id_user` = ?", (num, id_user))
            elif win == 3:
                return self.cursor.execute("UPDATE `users` SET `part` = ? WHERE `id_user` = ?", (num, id_user))
            elif win == 4:
                return self.cursor.execute("UPDATE `users` SET `city` = ? WHERE `id_user` = ?", (num, id_user))

    def get_subs(self, status=True):
        """Получаем всех подписчиков"""
        with self.connection:
            return [i[0] for i in self.cursor.execute("SELECT id_user FROM `users` WHERE `status` = ?",
                                                      (status,)).fetchall()]

    def get_send(self, send=True):
        """Получаем всех подписчиков"""
        with self.connection:
            return [i[0] for i in self.cursor.execute("SELECT id_user FROM `users` WHERE `send` = ?",
                                                      (send,)).fetchall()]

    def get_users(self, part, city):
        """Получаем всех подписчиков"""
        with self.connection:
            return [i[0] for i in self.cursor.execute("SELECT id_user FROM `users` WHERE `status` = ? AND `part` = ? AND `city` = ?",
                                                      (True, part, city)).fetchall()]

    def get_sends(self, part, city, send=True):
        """Получаем только подписчиков, только с полной или нет"""
        with self.connection:
            return [i[0] for i in self.cursor.execute("SELECT id_user FROM `users` WHERE `status` = ? AND `send` = ? AND `part` = ? AND `city` = ?",
                                                      (True, send, part, city)).fetchall()]

    def update_status(self, id_user):
        """Обновляем статус пользователя"""
        with self.connection:
            rat = self.cursor.execute("SELECT `rating` FROM `users` WHERE `id_user` = ?", (id_user, )).fetchone()
            if int(rat[0]) + 1 == 3:
                self.cursor.execute("UPDATE `users` SET `status` = ? WHERE `id_user` = ?", (0, id_user))
                self.cursor.execute("UPDATE `users` SET `rating` = ? WHERE `id_user` = ?", (0, id_user))
            else:
                self.cursor.execute("UPDATE `users` SET `rating` = ? WHERE `id_user` = ?", (int(rat[0]) + 1, id_user))
            return 1

    # ВЫЗОВ ДОПОЛНИТЕЛЬНЫХ ДАННЫХ
    def get_data(self):
        """Получаем данные"""
        with self.connection:
            data = self.cursor.execute("SELECT * FROM `data`").fetchone()
            return data[1], data[2]

    def update_data(self, data, part):
        """Обновляем данные"""
        with self.connection:
            self.cursor.execute("UPDATE `data` SET `date` = ? WHERE `id` = ?", (data, 1))
            self.cursor.execute("UPDATE `data` SET `part` = ? WHERE `id` = ?", (part, 1))
            return 1

    # СОХРАНЕНИЕ ДАННЫХ ОБ АКТИРОВКАХ
    def save_acta(self, city, part):
        """Обновляем данные"""
        with self.connection:
            for i, town in enumerate(["nor", "tal", "oga", "kae"]):
                self.cursor.execute(f"UPDATE `parts` SET `{town}` = ? WHERE `part` = ?", (city[i][1], part))
            return 1

    def get_acta(self, part):
        """Получаем данные"""
        city = []
        with self.connection:
            for town in ["nor", "tal", "oga", "kae"]:
                act = self.cursor.execute(f"SELECT `{town}` FROM `parts` WHERE `part` = ?", (part, )).fetchone()
                city.append(act[0])
            return city

    def del_acta(self):
        """Удаляем данные"""
        with self.connection:
            for part in [1, 2]:
                for town in ["nor", "tal", "oga", "kae"]:
                    self.cursor.execute(f"UPDATE `parts` SET `{town}` = ? WHERE `part` = ?", (None, part))
            pass

    def check_acta(self, part):
        """Проверяем данные"""
        with self.connection:
            for town in ["nor", "tal", "oga", "kae"]:
                z = self.cursor.execute(f"SELECT `{town}` FROM `parts` WHERE `part` = ?", (part, )).fetchone()
                if z[0] == None:
                    return 0
            return 1

    # ПОЛУЧЕНИЕ ДАННЫХ С GISMETEO
    def get_moments(self):
        """Получаем все дни"""
        with self.connection:
            return [i[0] for i in self.cursor.execute("SELECT `id` FROM `weather`").fetchall()]

    def update_weather(self, str_data, moment, time):
        """Обновляем данные"""
        with self.connection:
            return self.cursor.execute(f"UPDATE `weather` SET `{int(time)}` = ? WHERE `id` = ?", (f'{str_data}', moment))

    def get_weather(self, moment):
        """Отдаём сохранённые данные"""
        with self.connection:
            wthr = {}
            moments = [i[0] for i in self.cursor.execute("SELECT `id` FROM `weather`").fetchall()]
            for time in [1, 4, 7, 10, 13, 16, 19, 22]:
                dt = self.cursor.execute(f"SELECT `{time}` FROM `weather` WHERE `id` = ?",
                                         (moments[moment], )).fetchone()
                wthr[time] = eval(dt[0])
            return wthr

    # ВЫКЛЮЧЕНИЕ ВЫЗОВА
    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
