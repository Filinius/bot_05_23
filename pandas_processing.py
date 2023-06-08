import pandas as pd
import openpyxl


#df = pd.read_excel('Data/102.xlsx')
df = [1,2,3,4,5]
ser = pd.Series(df)
print(ser)

exercise = input("Введите название упражнения: ")
exercise_result = float(input("Введите результат упражнения: "))

rdf = df.loc[df[exercise] == exercise_result, 'points'].iloc[0]
print(rdf)