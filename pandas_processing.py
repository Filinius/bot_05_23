import pandas as pd
import openpyxl


df = pd.read_excel('Data/102.xlsx')
print(df)

exercise = input("Введите название упражнения: ")
exercise_result = float(input("Введите результат упражнения: "))

rdf = df.loc[df[exercise] == exercise_result, ['points']]
print(rdf)