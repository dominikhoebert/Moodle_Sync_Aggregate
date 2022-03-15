import pandas as pd
import re

# Nicht verwendet weil Klasseneinteilung veraltet.

dataframe = pd.read_excel("data/Klasseneinteilung_21-22_In_Arbeit_V2.xlsx", sheet_name=None, index_col=0, skiprows=0,
                          header=1)
students = {'Name': [], 'Klasse': []}
for klasse, df in dataframe.items():
    if klasse != 'Übersicht':
        for i, row in df.iterrows():
            name = re.sub(' +', ' ', row['Nachname Vorname'])
            students['Name'].append(name)
            if len(klasse) > 5:
                klasse = klasse[:5]
            students['Klasse'].append(klasse)

data = pd.DataFrame.from_dict(students)
data.to_csv("ldap_studentlist.csv", index=False)
