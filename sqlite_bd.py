import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.curs = self.conn.cursor()


    #async def connect(self):
        #self.conn = sqlite3.connect(self.db_file)

    async def create_table_user(self):
        self.curs.execute(
            'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, id_user INTEGER, exercise TEXT, exercise_result INTEGER)')
        self.conn.commit()

    def add_user(self, user_id):
        with self.conn:
            self.curs.execute("INSERT INTO users (id_user) VALUES (?)",(user_id,))



