import openpyxl
import sqlite3

# Открываем Excel-файл
workbook = openpyxl.load_workbook('102.xlsx')

# Получаем рабочий лист
sheet = workbook.active

# Подключаемся к базе данных
conn = sqlite3.connect('new.db')
c = conn.cursor()

# Создаем таблицу в базе данных
c.execute('''CREATE TABLE run_100
             (points INTEGER, run_100 FLOAT, pull_up INTEGER, marsh_for_5 FLOAT)''')


# Записываем данные в базу данных
for row in sheet.iter_rows(min_row=2, max_col=4, values_only=True):
    c.execute("INSERT INTO run_100 (points, run_100, pull_up, marsh_for_5) VALUES (?, ?, ?, ?)", row)


# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение с базой данных
conn.close()
