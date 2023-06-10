import pandas as pd
import openpyxl

df = pd.read_excel('Data/102.xlsx')

#print(df)
#print(df.dtypes)

exercise = input("Введите название упражнения: ")
exercise_result = float(input("Введите результат упражнения: "))

if exercise_result > df[exercise].min():
    if not any(df[exercise] == exercise_result):
        next_exercise_result = df.loc[df[exercise] < exercise_result, exercise].iloc[0] #знак < для значечий КОЛИЧЕСТВО
        next_exercise_points = df.loc[df[exercise] == next_exercise_result, 'points'].iloc[0]
        print(next_exercise_points)
    else:
        current_exercise_points = df.loc[df[exercise] == exercise_result, 'points'].iloc[0]
        print(current_exercise_points)
else:
    print("Результа меньше минимально допустимого. Упражнение не выполнено.")