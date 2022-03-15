import pandas as pd
import os

path = "data\klassenbuecher"
os.chdir(path)

students = {'Name': [], 'Klasse': []}
for file in os.listdir():
    if file.endswith(".xlsx"):
        file_path = f"{path}\{file}"
        df = pd.read_excel(file, sheet_name='UW16', index_col=None, skiprows=9, header=None, usecols='B')
        df.dropna(subset=[1], inplace=True)
        klasse = file[12:17]

        for i, row in df.iterrows():
            students['Name'].append(row[1])
            students['Klasse'].append(klasse)

data = pd.DataFrame.from_dict(students)
data.to_csv("ldap_studentlist.csv", index=False)
print(data)
