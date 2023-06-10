import pandas as pd
#import openpyxl



class PandasCalc:
    def __init__(self, path_df):
        self.df = pd.read_excel(path_df)


    def calc_result_time(self):
        pass

    def calc_result_reps(self, exercise: str, exercise_result: int):
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
            # Если есть значение полученного результата, то находим количество баллов.
            return exercise_points
