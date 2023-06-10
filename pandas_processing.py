import pandas as pd
#import openpyxl



class PandasCalc:
    def __init__(self, path_df):
        self.df = pd.read_excel(path_df)


    def calc_result_time(self, exercise, exercise_result):
        if exercise_result > self.df[exercise].max():
            return f"Результа больше максимально допустимого. Упражнение не выполнено."

        # Проверяем есть ли в столбце "exercise" какое-либо значение, равное переменной "exercise_result".
        if not any(self.df[exercise].eq(exercise_result)):
            #Переменная "next_exercise_result" будет содержать значение первой строки в столбце "exercise", которое больше значения переменной "exercise_result".
            next_exercise_result = self.df.loc[self.df[exercise] > exercise_result, exercise].iloc[0] # (знак > для значечий, где время в упражнении).
            exercise_points = self.df.loc[self.df[exercise] == next_exercise_result, 'points'].iloc[0]
            # Получаем количество баллов.
            return exercise_points


    def calc_result_reps(self, exercise, exercise_result):
        # Проверяем, больше ли значение переменной "exercise_result" минимального значения в столбце "exercise" в df.
        if exercise_result < self.df[exercise].min():
            return f"Результа меньше минимально допустимого. Упражнение не выполнено."

        # Проверяем есть ли в столбце "exercise" какое-либо значение, равное переменной "exercise_result".
        if not any(self.df[exercise].eq(exercise_result)):
            #Переменная "next_exercise_result" будет содержать значение первой строки в столбце "exercise", которое меньше значения переменной "exercise_result".
            next_exercise_result = self.df.loc[self.df[exercise] < exercise_result, exercise].iloc[0] # (знак < для значечий, где КОЛИЧЕСТВО повторений в упражнении).
            exercise_points = self.df.loc[self.df[exercise] == next_exercise_result, 'points'].iloc[0]
            # Получаем количество баллов.
            return exercise_points

        else:
            exercise_points = self.df.loc[self.df[exercise] == exercise_result, 'points'].iloc[0]
            # Если есть значение полученного результата "exercise_result", то находим количество баллов.
            return exercise_points
