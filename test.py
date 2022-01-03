import pandas as pd
from moodle_sync import MoodleSync


studentlist = pd.read_csv('data/studentlist.csv')

moodle = MoodleSync("https://elearning.tgm.ac.at", "394885eab4902cb2bbff605b6be6330f")

grades = moodle.get_gradereport_of_course(5393)
#print(grades)

grades[['a', 'b', 'c']] = grades['Schüler'].str.split(' ', 2, expand=True)
grades['Name2'] = grades['a'] + ' ' + grades['b']

studentlist[['a', 'b', 'c']] = studentlist['Name'].str.split(' ', 2, expand=True)
studentlist['Name3'] = studentlist['a'] + ' ' + studentlist['b']

#print(grades['Name2'].head())



grades = grades.merge(studentlist, how='left', left_on='Name2', right_on='Name3')
g=grades[['Schüler', 'Klasse']]

print(g)
