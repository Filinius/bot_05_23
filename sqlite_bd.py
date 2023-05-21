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
            'exercise TEXT, exercise_result INTEGER)')
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
