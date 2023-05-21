import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.curs = self.conn.cursor()

    # async def connect(self):
    # self.conn = sqlite3.connect(self.db_file)

    async def create_table_user(self):
        self.curs.execute(
            'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, user_id INTEGER, full_name TEXT, '
            'exercise TEXT, exercise_result FLOAT)')
        self.conn.commit()

    def add_id_user_full_name(self, user_id, full_name):
        with self.conn:
            self.curs.execute("INSERT INTO users (user_id, full_name) VALUES (?, ?)", (user_id, full_name))
            self.conn.commit()

    def add_user(self, user_id, full_name):
        with self.conn:
            self.curs.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
            user = self.curs.fetchone()
            if not user:
                self.curs.execute("INSERT INTO users (user_id, full_name) VALUES (?, ?)", (user_id, full_name))
            else:
                return False

    def add_exercise_exercise_result(self, exercise, exercise_result, user_id):
        with self.conn:
            self.curs.execute("UPDATE users SET exercise=?, exercise_result=? WHERE user_id = ?", (exercise, exercise_result, user_id))
            #self.curs.execute("INSERT INTO users (exercise, exercise_result) VALUES (?,?)", (exercise, exercise_result))
            self.conn.commit()

    def calc_result(self, exercise):
        with self.conn:
            self.curs.execute(
                "SELECT points FROM {} INNER JOIN users ON {}.exercise_result = users.exercise_result".format(exercise, exercise))
            result = self.curs.fetchone()
            self.conn.commit()
        return result

    # def calc_result(self):
    #     with self.conn:
    #         self.curs.execute("SELECT points FROM run_100 INNER JOIN users ON run_100.exercise_result = users.exercise_result")
    #         self.conn.commit()
"""
SELECT users.name, orders.order_date
FROM users
INNER JOIN orders ON users.id = orders.user_id;
Этот запрос выберет имена пользователей и даты их заказов и свяжет их по полю "id" в таблице "users" и полю "user_id" в 
таблице "orders". Если вы хотите, чтобы результаты были отфильтрованы по определенному условию, вы можете добавить 
оператор WHERE:
"""
